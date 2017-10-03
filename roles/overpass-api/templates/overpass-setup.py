#!/usr/bin/env python3

import hashlib
import logging
import os
import re
import subprocess
import sys
import time
from datetime import datetime, timedelta
from urllib.request import urlretrieve

import requests

from systemd.journal import JournalHandler


def parse_state_txt(url):
    resp = requests.get(url)

    for line in resp.text.split('\n'):
        if line.startswith('sequenceNumber'):
            sequence_number = line.split('=')[1]
        elif line.startswith('timestamp'):
            timestamp = line.split('=')[1]

    return (sequence_number, datetime.strptime(timestamp[:-5], '%Y-%m-%dT%H\:%M'))


def md5(fname):
    hash_md5 = hashlib.md5()
    with open(fname, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()


log = logging.getLogger('overpass-setup.py')
log.addHandler(JournalHandler())
log.setLevel(logging.INFO)


log.info('retrieve latest pbf date')
resp = requests.get('{{ overpass_pbf_root_url }}')
pbf_prog = re.compile(r'^.*<img src="/icons/unknown\.gif".*<a href="{{ overpass_pbf_region }}-(\d{6})\.osm\.pbf">.*$')
dts = []
for line in resp.text.split('\n'):
    m = pbf_prog.match(line)
    if m:
        dts.append(datetime.strptime(m.group(1), '%y%m%d'))
pbf_datetime = max(dts)


log.info('look for first replication update')
if "{{ overpass_replication_interval }}" == "minute":
    delta = timedelta(minutes=1)
    divider = 60
    max_interval = 10
elif "{{ overpass_replication_interval }}" == "day":
    delta = timedelta(days=1)
    divider = 3600 * 24
    max_interval = 25 * 60
else:
    log.error('overpass_replication_interval must be minute or day')
    sys.exit(2)

obj_datetime = pbf_datetime - delta
url = '{{ overpass_replication_url }}/state.txt'

repl_seq, repl_datetime = parse_state_txt(url)
diff_datetime = obj_datetime - repl_datetime
while diff_datetime > timedelta(minutes=max_interval) or diff_datetime < timedelta(minutes=0):
    repl_seq = '{:09}'.format(int(repl_seq) + int(diff_datetime.total_seconds() // divider))
    url = '{{ overpass_replication_url }}/{}/{}/{}.state.txt'.format(repl_seq[:-6], repl_seq[-6:-3], repl_seq[-3:])
    repl_seq, repl_datetime = parse_state_txt(url)
    diff_datetime = obj_datetime - repl_datetime


log.info('download pbf')
pbf_url = '{{ overpass_pbf_root_url }}/{{ overpass_pbf_region }}-{}.osm.pbf'.format(pbf_datetime.strftime('%y%m%d'))
pbf_dest = '{{ overpass_database_dir }}/{{ overpass_pbf_region }}-{}.osm.pbf'.format(pbf_datetime.strftime('%y%m%d'))

if not os.path.exists(pbf_dest):
    urlretrieve(pbf_url, pbf_dest)

resp = requests.get(pbf_url + '.md5')
md5_osm = resp.text.split()[0]
if md5(pbf_dest) != md5_osm:
    log.critical('md5 differ')
    sys.exit(1)


log.info('install database')
try:
    subprocess.check_call(
        'osmconvert {} --out-osm | update_database --db-dir={{ overpass_database_dir }} --meta'.format(pbf_dest),
        shell=True,
    )
except:
    log.critical('install database failed')
    sys.exit(2)

time.sleep(1)
log.info('wait update_database')
while not subprocess.call(['/bin/pidof', 'update_database']):
    time.sleep(1)

log.info('delete pbf')
os.remove(pbf_dest)

log.info('write replicate_id')
with open('{{ overpass_database_dir }}/replicate_id', 'w') as fd:
    fd.write(repl_seq)

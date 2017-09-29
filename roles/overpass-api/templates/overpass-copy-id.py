#!/usr/bin/env python3

import logging

from systemd.journal import JournalHandler

log = logging.getLogger('overpass-setup.py')
log.addHandler(JournalHandler())
log.setLevel(logging.INFO)

log.info('write first_replicate_id')
with open('{{ overpass_database_dir }}/replicate_id') as fd:
    rid = fd.readline()

with open('{{ overpass_database_dir }}/first_replicate_id', 'w') as fd:
    fd.write('ID=%s' % rid)

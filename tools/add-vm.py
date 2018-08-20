#! /usr/bin/python3

import argparse
import os
import sys

host_config = {
  "osm26": {
    "hostname": "osm26.openstreetmap.fr",
    "ipv4": "10.0.0.26",
    "ipv6": "2001:41d0:1008:1f65:1::26",
  },
  "osm27": {
    "hostname": "osm27.openstreetmap.fr",
    "ipv4": "10.0.0.27",
    "ipv6": "2001:41d0:1008:1f84:1::27",
  },
  "osm28": {
    "hostname": "osm28.openstreetmap.fr",
    "ipv4": "10.0.0.28",
    "ipv6": "2001:41d0:1008:2c6b:1::28",
  },
}

templates = [
  "debian-9.0-standard_9.3-1_amd64.tar.gz",
  "ubuntu-18.04-standard_18.04-1_amd64.tar.gz",
]

storages = [
  "hdd-sdd",
  "ceph",
  "local",
]

default_template = templates[0]
default_cpus = 1
default_memory = 1024
default_disk = 10
default_storage = storages[0]

def parse_args():

  parser = argparse.ArgumentParser(description='Create configuration for a new VM.')

  parser.add_argument('--host',     action='store', choices=host_config.keys())
  parser.add_argument('--vmid',     action='store', type=int,
                      help="default: automatically guessed from ./hosts")
  parser.add_argument('--template', action='store', default=default_template,
                      help="default: %(default)s")

  parser.add_argument('--cpus',    action='store', type=int, default=default_cpus,
                      help="default: %(default)s")
  parser.add_argument('--memory',  action='store', type=int, default=default_memory,
                      help="default: %(default)s Mio")
  parser.add_argument('--disk',    action='store', type=int, default=default_disk,
                      help="default: %(default)s Gio")
  parser.add_argument('--storage', action='store', choices=storages, default=default_storage,
                      help="default: %(default)s")

  parser.add_argument('--force', action='store_true', help="Force creation of VM without confirmation")

  args = parser.parse_args()

  return args


def find_vmid(vmid=None):

  existing_names = set()

  with open("hosts") as f:
    for line in f:
      if line.startswith("osm"):
        name = int(line.split(".")[0].split("m")[1])
        existing_names.add(name)

  if vmid is None:
    vmid = max([vmid for vmid in existing_names if vmid < 200]) + 1

  if vmid in existing_names:
    raise Exception("VMID %s is already present in ./hosts" % vmid)

  return (vmid, existing_names)


def get_host(host=None):

  if host is not None:
    return host

  hosts = {}
  i = 0
  for h in sorted(host_config.keys()):
    hosts[i] = h
    i += 1

  while host is None:
    print("Choose host:")
    for i in sorted(hosts.keys()):
      print("%d) %s" % (i, hosts[i]))

    try:
      resp = int(input("? "))
      host = hosts[resp]
    except (ValueError, IndexError) as e:
      print("- Incorrect answer\n")

  return host


def expand_args(args):

  if args.vmid > 255:
    raise Exception("vmid > 255 not supported for ipv4 calculation")
  args.ipv4 = "10.0.0.%d" % args.vmid

  args.ipv6 = ":".join(host_config[args.host]["ipv6"].split(":")[:-1]) + ":%d" % args.vmid

  args.netif = '{"net0": "name=eth0,bridge=vmbr0,ip=%(ipv4)s/24,gw=%(ipv4_h)s,ip6=%(ipv6)s/80,gw6=%(ipv6_h)s"}' % {"ipv4": args.ipv4, "ipv4_h": host_config[args.host]["ipv4"], "ipv6": args.ipv6, "ipv6_h": host_config[args.host]["ipv6"]}

  args.swap = "2048"

  args.dns_name = "osm%s.openstreetmap.fr" % args.vmid

  return args


def print_config(args):

  print("VMID %d" % args.vmid)
  print("--------")
  print("dns:      %s" % args.dns_name)
  print("host:     %s" % args.host)
  print("cpus:     %s" % args.cpus)
  print("memory:   %s Mio" % args.memory)
  print("disk:     %s Gio on %s" % (args.disk, args.storage))
  print("ipv6:     %s" % args.ipv6)
  print("template: %s" % args.template)
  print("--------")


def configure_ansible(args):

  host_var_proxmox = "host_vars/%s/proxmox" % args.dns_name

  if os.path.isfile(host_var_proxmox):
    raise Exception("File '%s' already present" % host_var_proxmox)

  try:
    os.mkdir(os.path.dirname(host_var_proxmox))
  except FileExistsError:
    pass

  with open(host_var_proxmox, "xt") as f:
    f.write("proxmox_var:\n")
    f.write("  host: %s\n" % host_config[args.host]["hostname"])
    f.write("  cpus: %s\n" % args.cpus)
    f.write("  disk: %s\n" % args.disk)
    f.write("  ipv6: %s\n" % args.ipv6)
    f.write("  netif: %s\n" % args.netif)
    f.write("  memory: %s\n" % args.memory)
    f.write("  ostemplate: %s\n" % args.template)
    f.write("  storage: \"%s\"\n" % args.storage)
    f.write("  swap: %s\n" % args.swap)
    f.write("  vmid: %s\n" % args.vmid)


  hosts_tmp = "hosts.tmp"

  with open("hosts", "rt") as f_h:
    with open(hosts_tmp, "xt") as f:
      add_vm = False
      for line in f_h:
        if line.startswith("[vm"):
          add_vm = True
        elif line.startswith("["):
          add_vm = False

        if add_vm and line.startswith("osm"):
          name = int(line.split(".")[0].split("m")[1])
          if name > args.vmid:
            f.write("%s vm_host=%s\n" % (args.dns_name, host_config[args.host]["hostname"]))
            add_vm = False

        f.write(line)

  os.rename(hosts_tmp, "hosts")


if __name__ == '__main__':
  args = parse_args()
  (args.vmid, existing_names) = find_vmid(args.vmid)
  args.host = get_host(args.host)
  args = expand_args(args)
  print_config(args)

  if not args.force:
    resp = input("Confirm [y/N] ? ")
    if resp not in ("y", "Y"):
      print("- cancelled")
      sys.exit(1)

  configure_ansible(args)


#! /usr/bin/env python3

import argparse
import os
import re
import sys
from termcolor import colored

host_config = {
  "osm11": {
    "hostname": "osm11.openstreetmap.fr",
    "bridge": "vmbr1",
    "gw4":  "192.168.0.254",
    "ipv4": "192.168.%d.%d",
    "gw6": "2a01:e0d:1:c:58bf:fac1:8000:11",
    "ipv6": "2a01:e0d:1:c:58bf:fac1:8000:%d",
    "default_storage": "ssd-zfs",
  },
  "osm12": {
    "hostname": "osm12.openstreetmap.fr",
    "bridge": "vmbr2",
    "gw4":  "10.0.0.12",
    "ipv4": "10.1.%d.%d",
    "gw6": "2a01:e0d:1:c:58bf:fac1:c200:12",
    "ipv6": "2a01:e0d:1:c:58bf:fac1:c200:%d",
    "default_storage": "ssd-zfs",
  },
  "osm14": {
    "hostname": "osm14.openstreetmap.fr",
    "bridge": "vmbr2",
    "gw4":  "10.0.0.14",
    "ipv4": "10.1.%d.%d",
    "gw6": "2a01:e0d:1:c:58bf:fac1:c400:14",
    "ipv6": "2a01:e0d:1:c:58bf:fac1:c400:%d",
    "default_storage": "ssd-zfs",
  },
  "osm26": {
    "hostname": "osm26.openstreetmap.fr",
    "bridge": "vmbr0",
    "gw4":  "10.0.0.26",
    "ipv4": "10.1.%d.%d",
    "gw6": "2001:41d0:1008:1fff:ff:ff:ff:ff",
    "ipv6": "2001:41d0:1008:1f65:1::%d",
    "default_storage": "local-zfs",
  },
  "osm27": {
    "hostname": "osm27.openstreetmap.fr",
    "bridge": "vmbr0",
    "gw4":  "10.0.0.27",
    "ipv4": "10.1.%d.%d",
    "gw6":  "2001:41d0:1008:1fff:ff:ff:ff:ff",
    "ipv6": "2001:41d0:1008:1f84:1::%d",
    "default_storage": "local-zfs",
  },
  "osm28": {
    "hostname": "osm28.openstreetmap.fr",
    "bridge": "vmbr0",
    "gw4":  "10.0.0.28",
    "ipv4": "10.1.%d.%d",
    "gw6":  "2001:41d0:1008:2cff:ff:ff:ff:ff",
    "ipv6": "2001:41d0:1008:2c6b:1::%d",
    "default_storage": "local-zfs",
  },
  "osm29": {
    "hostname": "osm29.openstreetmap.fr",
    "bridge": "vmbr0",
    "gw4":  "10.42.109.1",
    "ipv4": "10.42.109.%d",
    "gw6":  "2a00:1788:100:109::1",
    "ipv6": "2a00:1788:100:109::%d",
    "default_storage": "local-zfs",
  },
  "osm30": {
    "hostname": "osm30.openstreetmap.fr",
    "bridge": "vmbr0",
    "gw4":  "10.42.109.1",
    "ipv4": "10.42.109.%d",
    "gw6":  "2a00:1788:100:109::1",
    "ipv6": "2a00:1788:100:109::%d",
    "default_storage": "local-zfs",
  },
  "osm31": {
    "hostname": "osm31.openstreetmap.fr",
    "bridge": "vmbr0",
    "gw4":  "10.42.109.1",
    "ipv4": "10.42.109.%d",
    "gw6":  "2a00:1788:100:109::1",
    "ipv6": "2a00:1788:100:109::%d",
    "default_storage": "local-zfs",
  },
  "osm32": {
    "hostname": "osm32.openstreetmap.fr",
    "bridge": "vmbr0",
    "bridge_ipv6": "vmbr1",
    "gw4":  "10.0.0.32",
    "ipv4": "10.1.%d.%d",
    "gw6":  "2001:67c:1740:9031::1",
    "ipv6": "2001:67c:1740:9031::%d",
    "default_storage": "local-zfs",
  },
  "osm33": {
    "hostname": "osm33.openstreetmap.fr",
    "bridge": "vmbr0",
    "bridge_ipv6": "vmbr1",
    "gw4":  "10.0.0.33",
    "ipv4": "10.1.%d.%d",
    "gw6":  "2001:67c:1740:9031::1",
    "ipv6": "2001:67c:1740:9031::%d",
    "default_storage": "local-zfs",
  },
  "osm34": {
    "hostname": "osm34.openstreetmap.fr",
    "bridge": "vmbr0",
    "bridge_ipv6": "vmbr1",
    "gw4":  "10.0.0.34",
    "ipv4": "10.1.%d.%d",
    "gw6":  "2001:67c:1740:9031::1",
    "ipv6": "2001:67c:1740:9031::%d",
    "default_storage": "local-zfs",
  },
  "osm35": {
    "hostname": "osm35.openstreetmap.fr",
    "bridge": "vmbr0",
    "bridge_ipv6": "vmbr1",
    "gw4":  "10.0.0.35",
    "ipv4": "10.1.%d.%d",
    "gw6":  "2001:67c:1740:9031::1",
    "ipv6": "2001:67c:1740:9031::%d",
    "default_storage": "local-zfs",
  },
  "osm36": {
    "hostname": "osm36.openstreetmap.fr",
    "bridge": "vmbr0",
    "bridge_ipv6": "vmbr1",
    "gw4":  "10.0.0.36",
    "ipv4": "10.1.%d.%d",
    "gw6":  "2001:67c:1740:9031::1",
    "ipv6": "2001:67c:1740:9031::%d",
    "default_storage": "local-zfs",
  },
}

templates = [
  "debian-12-standard_12.2-1_amd64.tar.zst",
  "debian-11-standard_11.6-1_amd64.tar.zst",
  "debian-10-standard_10.7-1_amd64.tar.gz",
  "debian-9.0-standard_9.7-1_amd64.tar.gz",
  "ubuntu-18.04-standard_18.04-1_amd64.tar.gz",
]

templates_kvm = [
  "debian-11-genericcloud-amd64"
]

storages = [
  "hdd-sdd",
  "hdd-zfs",
  "ceph",
  "local",
  "local-zfs",
  "ssd-nvme",
  "ssd-sata",
  "ssd-zfs",
]

default_template = templates[0]
default_cpus = 1
default_memory = 1024
default_disk = 10


def parse_args():

  parser = argparse.ArgumentParser(description='Create configuration for a new VM.')

  parser.add_argument('--host',     action='store', choices=host_config.keys())
  parser.add_argument('--vmid',     action='store', type=int,
                      help="default: automatically guessed from ./hosts")
  parser.add_argument('--vmname',     action='store', type=str,
                      help="Name for VM in DNS, will be suffixed by .vm.openstreetmap.fr - default: osmVMID")
  parser.add_argument('--template', action='store', default=default_template,
                      help="default: %(default)s")

  parser.add_argument('--cpus',    action='store', type=int, default=default_cpus,
                      help="default: %(default)s")
  parser.add_argument('--memory',  action='store', type=int, default=default_memory,
                      help="default: %(default)s Mio")
  parser.add_argument('--disk',    action='store', type=int, default=default_disk,
                      help="default: %(default)s Gio")
  parser.add_argument('--storage', action='store', choices=storages,
                      help="default: %(default)s")
  parser.add_argument('--user', action='append', type=str,
                      help="Users to create, with root access")
  parser.add_argument('--docker',    action='store_true', default=False,
                      help="Enable docker support")
  parser.add_argument('--kvm',    action='store_true', default=False,
                      help="Create a KVM instead of a LXC container")

  parser.add_argument('--force', action='store_true', help="Force creation of VM without confirmation")

  args = parser.parse_args()

  return args


def find_vmid(vmid=None, vmname=None):

  existing_vmid = set()
  existing_names = set()

  with open("hosts") as f:
    re_osm = re.compile(r"osm([0-9]+)\.")
    re_vm_openstreetmap_fr = re.compile(r"([0-9a-z_.]+)\.openstreetmap\.fr")

    for line in f:
      ms = re_osm.findall(line)
      for m in ms:
        existing_vmid.add(int(m))
      ms = re_vm_openstreetmap_fr.findall(line)
      for m in ms:
        existing_names.add(m)

  if vmid is None:
    vmid = max([vmid for vmid in existing_vmid if vmid < 211]) + 1

  if vmname is None:
    vmname = "osm%d" % vmid
  else:
    vmname = "%s.vm" % vmname

  if vmid in existing_vmid:
    raise Exception("VMID %s is already present in ./hosts" % vmid)

  if vmname in existing_names:
    raise Exception("VM name %s is already present in ./hosts" % vmname)

  return (vmid, vmname)


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
    except (ValueError, IndexError):
      print("- Incorrect answer\n")

  return host


def compute_ipv4(cfg_host, vmid):

  if cfg_host["ipv4"].count("%d") == 1 and vmid > 255:
    raise Exception("vmid > 255 not supported for ipv4 calculation")

  if cfg_host["ipv4"].count("%d") == 1:
    return cfg_host["ipv4"] % vmid
  else:
    return cfg_host["ipv4"] % (vmid // 256, vmid % 256)


def compute_ipv4_prefix(cfg_host, vmid):
  return "24"


def compute_ipv6(cfg_host, vmid):

  if vmid > 9999:
    raise Exception("vmid > 9999 not supported for ipv6 calculation")

  return cfg_host["ipv6"] % vmid


def compute_ipv6_prefix(cfg_host, vmid):
  return "80"


def expand_args(args):

  cfg_host = host_config[args.host]

  args.ipv4 = compute_ipv4(cfg_host, args.vmid)
  args.ipv6 = compute_ipv6(cfg_host, args.vmid)
  args.ipv4_prefix = compute_ipv4_prefix(cfg_host, args.vmid)
  args.ipv6_prefix = compute_ipv6_prefix(cfg_host, args.vmid)

  if args.kvm:
    if "bridge_ipv6" not in cfg_host:
      raise Exception("kvm not supported without bridge_ipv6 in host")

    args.net  = '{"net0": "bridge=%(bridge)s",' % {"bridge": cfg_host["bridge"]}
    args.net += ' "net1": "bridge=%(bridge_ipv6)s"}' % {"bridge_ipv6": cfg_host["bridge_ipv6"]}

    args.ipconfig  = '{"ipconfig0": "ip=%(ipv4)s/24,gw=%(gw4)s",' % {"ipv4": args.ipv4, "gw4": cfg_host["gw4"]}
    args.ipconfig += ' "ipconfig1": "ip6=%(ipv6)s/128,gw6=%(gw6)s"}' % {"ipv6": args.ipv6, "gw6": cfg_host["gw6"]}

  else:
    if "bridge_ipv6" in cfg_host:
      args.netif  = '{"net0": "name=eth0,bridge=%(bridge)s,ip=%(ipv4)s/%(ipv4_prefix)s,gw=%(gw4)s",' % {"bridge": cfg_host["bridge"], "ipv4": args.ipv4, "ipv4_prefix": args.ipv4_prefix, "gw4": cfg_host["gw4"]}
      args.netif += ' "net1": "name=eth1,bridge=%(bridge_ipv6)s,ip6=%(ipv6)s/%(ipv6_prefix)s,gw6=%(gw6)s"}' % {"bridge_ipv6": cfg_host["bridge_ipv6"], "ipv6": args.ipv6, "ipv6_prefix": args.ipv6_prefix, "gw6": cfg_host["gw6"]}
    else:
      args.netif = '{"net0": "name=eth0,bridge=%(bridge)s,ip=%(ipv4)s/24,gw=%(gw4)s,ip6=%(ipv6)s/97,gw6=%(gw6)s"}' % {"bridge": cfg_host["bridge"], "ipv4": args.ipv4, "gw4": cfg_host["gw4"], "ipv6": args.ipv6, "gw6": cfg_host["gw6"]}

  args.swap = "2048"

  args.dns_name = "%s.openstreetmap.fr" % args.vmname

  if not args.storage:
    args.storage = host_config[args.host]["default_storage"]

  if args.docker and args.disk < 50:
    print(colored("WARNING: Increasing diskspace to 50G for docker usage", "yellow"))
    args.disk = 50

  if args.kvm and args.template not in templates_kvm:
    print(colored("WARNING: Changing template for kvm to {0}".format(templates_kvm[0]), "yellow"))
    args.template = templates_kvm[0]

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
  if args.user:
    print("user_root: %s" % args.user)
  if args.docker:
    print("docker   : yes")
  if args.kvm:
    print("kvm      : yes")
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
    f.write("  docker: %s\n" % int(args.docker))
    f.write("  hostname: %s\n" % args.dns_name)
    f.write("  ipv6: %s\n" % args.ipv6)
    f.write("  kvm: %s\n" % int(args.kvm))
    if args.kvm:
      f.write("  net: %s\n" % args.net)
      f.write("  ipconfig: %s\n" % args.ipconfig)
    else:
      f.write("  netif: %s\n" % args.netif)
    f.write("  memory: %s\n" % args.memory)
    f.write("  ostemplate: %s\n" % args.template)
    f.write("  storage: \"%s\"\n" % args.storage)
    f.write("  swap: %s\n" % args.swap)
    f.write("  vmid: %s\n" % args.vmid)

  if args.user:
    user_var_proxmox = "host_vars/%s/users_root" % args.dns_name
    with open(user_var_proxmox, "xt") as f:
      f.write("users_root:\n")
      for user in args.user:
        f.write("  - %s\n" % user)

  hosts_tmp = "hosts.tmp"

  with open("hosts", "rt") as f_h:
    re_osm = re.compile(r"osm([0-9]+)\.")
    with open(hosts_tmp, "xt") as f:
      add_vm = False
      add_user = False
      for line in f_h:
        if line.startswith("[vm"):
          add_vm = True
        elif line.startswith("["):
          add_vm = False
          name = line[1:].split("]")[0]
          if args.user:
            for user in args.user:
              if user == name:
                add_user = True

        elif add_vm:
          ms = re_osm.findall(line)
          name = -1
          for m in ms:
            name = max(name, int(m))
          if name == -1 or name > args.vmid:
            f.write("%s vm_host=%s # osm%d.openstreetmap.fr\n" % (args.dns_name, host_config[args.host]["hostname"], args.vmid))
            add_vm = False

        elif add_user:
          if line == "\n" or line > args.dns_name:
            f.write("%s\n" % args.dns_name)
            add_user = False

        f.write(line)

  os.rename(hosts_tmp, "hosts")


if __name__ == '__main__':
  args = parse_args()
  (args.vmid, args.vmname) = find_vmid(args.vmid, args.vmname)
  args.host = get_host(args.host)
  args = expand_args(args)
  print_config(args)

  if not args.force:
    resp = input("Confirm [y/N] ? ")
    if resp not in ("y", "Y"):
      print("- cancelled")
      sys.exit(1)

  configure_ansible(args)

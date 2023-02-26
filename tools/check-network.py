#! /usr/bin/python

import copy
import dns.resolver
import os
import re
import subprocess
import sys
from termcolor import colored


class CheckNetwork:

  def __init__(self, read_proxmox=False, update_proxmox=False, update_dns=True):

    self.read_proxmox = read_proxmox
    self.update_proxmox = update_proxmox
    self.update_dns = update_dns

    if read_proxmox or update_proxmox:
      import proxmoxer
      self.proxmox = proxmoxer.ProxmoxAPI("osm26.openstreetmap.fr", user=os.getlogin(), backend="ssh_paramiko", sudo=True)

    if update_dns:
      self.gandi_api = None

    from importlib import import_module
    self.add_vm = import_module("add-vm")
    self.host_config = self.add_vm.host_config
    self.max_field_width = max([max(len(n["gw4"]), len(n["gw6"])) for n in self.host_config.values()])

  def read_config(self, path=None, vmid_checked=None, sudo=False):

    lxc_config = {}

    if path:
      p_nodes = os.path.join(args.path, "nodes")
      for node in sorted(os.listdir(p_nodes)):
        lxc_config[node] = {}
        p_lxc = os.path.join(p_nodes, node, "lxc")
        for f in sorted(os.listdir(p_lxc)):
          vmid = int(f.split(".")[0])
          if args.vmid is not None and args.vmid != vmid:
            continue
          lxc_config[node][vmid] = cn.get_lxc_config(os.path.join(p_lxc, f), sudo)

    else:
      for n in self.proxmox.nodes.get():
        if n["status"] == "offline":
          continue
        node = n["node"]
        lxc_config[node] = {}
        for l_c in self.proxmox.nodes(node).lxc.get():
          vmid = int(l_c["vmid"])
          if vmid_checked is not None and vmid_checked != vmid:
            continue
          cfg = self.proxmox.nodes(node).lxc(vmid).config.get()
          cfg['net0'] = dict((k, v) for k, v in (item.split("=") for item in cfg['net0'].split(",")))
          lxc_config[node][vmid] = cfg

    self.lxc_config = lxc_config
    return lxc_config

  def get_lxc_config(self, lxc_conf_file, sudo=False):

    cfg = {}

    if sudo:
      f = subprocess.check_output(["sudo", "cat", lxc_conf_file], encoding="utf-8").splitlines()
    else:
      f = open(lxc_conf_file)

    for line in f:
      if line.startswith("["):
        break
      elif ":" in line:
        (k, v) = line.split(": ")
        cfg[k.strip()] = v.strip()

    cfg['net0'] = dict((k, v) for k, v in (item.split("=") for item in cfg['net0'].split(",")))

    if not sudo:
      f.close()

    return cfg

  def check_config(self, vmid_checked=False):
    no_error = True
    for node in cfg.keys():
      for vmid in self.lxc_config[node].keys():
        if vmid_checked is not None and vmid_checked != vmid:
          continue
        if not cn.check_network_config(node, self.lxc_config[node][vmid], vmid):
          no_error = False
          print("")

    return no_error

  def check_dns_config(self, node, config, vmid):

    try:
      dns.resolver.resolve(config["hostname"], 'CNAME')
      print("%s/%s - %-30s - %s" % (node, vmid, config["hostname"], colored("skipped as with CNAME", "green")))
      return False
    except dns.resolver.NXDOMAIN:
      print("%s/%s - %-30s - %s" % (node, vmid, config["hostname"], colored("not configured", "yellow")))
      return False
    except dns.resolver.NoAnswer:
      pass

    s = dns.resolver.resolve(config["hostname"], 'AAAA')
    got_ip = s[0].address
    exp_ip = config['net0']['ip6'].split("/")[0].strip()
    if got_ip != exp_ip:
      print("%s/%s - %-30s - got: %s - exp: %s" % (node, vmid, config["hostname"], colored(got_ip, "yellow"), colored(exp_ip, "green")))

      if self.update_dns and config["hostname"].endswith(".openstreetmap.fr"):
        if input("Confirm DNS update [y/n]? ").lower() == "y":
          api_key = os.environ["GANDI_APIKEY"]

          if self.gandi_api is None:
            import modules.gandi
            self.gandi_api = modules.gandi.GandiAPI("openstreetmap.fr", api_key)
          if self.gandi_api.update_ipv6(config["hostname"].removesuffix(".openstreetmap.fr"), exp_ip):
            print(colored("  - updated", "green"))
          else:
            print("  - was already updated")
          return True

      return False

    return True

  def check_network_config(self, node, config, vmid):

    no_error = True
    skip_dns_check = False
    max_width = self.max_field_width + len(colored("", "yellow"))

    config_updated = copy.deepcopy(config)

    # Check gateway
    for (c1, c2) in [("gw", "gw4"), ("gw6", "gw6")]:
      got_cfg = config['net0'][c1]
      exp_cfg = self.host_config[node][c2]
      if got_cfg != exp_cfg:
        no_error = False
        config_updated['net0'][c1] = exp_cfg
        print("%s/%s - %-3s - got: %-*s - exp: %s" % (node, vmid, c1, max_width, colored(got_cfg, "yellow"), colored(exp_cfg, "green")))

    # Check IP
    for (c1, c2) in [("ip", "ipv4"), ("ip6", "ipv6")]:
      got_cfg = config['net0'][c1]
      if c2 == "ipv4":
        exp_cfg = self.add_vm.compute_ipv4(self.host_config[node], vmid) + "/" + self.add_vm.compute_ipv4_prefix(self.host_config[node], vmid)
      else:
        exp_cfg = self.add_vm.compute_ipv6(self.host_config[node], vmid) + "/" + self.add_vm.compute_ipv6_prefix(self.host_config[node], vmid)

      if got_cfg != exp_cfg:
        no_error = False
        config_updated['net0'][c1] = exp_cfg
        print("%s/%s - %-3s - got: %-*s - exp: %s" % (node, vmid, c1, max_width, colored(got_cfg, "yellow"), colored(exp_cfg, "green")))
        skip_dns_check = True

    if not no_error and self.update_proxmox:
      proxmox_net = self.proxmox.nodes(node).lxc(vmid).config.get()["net0"]
      proxmox_net_updated = ",".join([f"{k}={v}" for k, v in config_updated['net0'].items()])
      print(proxmox_net)
      print(proxmox_net_updated)
      if proxmox_net == proxmox_net_updated:
        print("  - was already updated")
      elif input("Confirm proxmox update [y/n]? ").lower() == "y":
        self.proxmox.nodes(node).lxc(vmid).config.put(net0=proxmox_net_updated)
        print(colored("  - updated", "green"))

    if config["hostname"].endswith(".vm.openstreetmap.fr") or re.match("^osm[0-9]*.openstreetmap.fr", config["hostname"]):
      if skip_dns_check:
        print("%s/%s - %-30s - %s" % (node, vmid, config["hostname"], colored("skipped", "yellow")))
      else:
        no_error &= self.check_dns_config(node, config, vmid)

    return no_error


def parse_args():

  import argparse

  parser = argparse.ArgumentParser(description='Check network configuration')
  group = parser.add_mutually_exclusive_group(required=True)
  group.add_argument('--read-proxmox', action='store_true', help="Read configuration from proxmox")
  group.add_argument('--path',         action='store', help="Read configuration from filesystem, like /etc/pve/")

  parser.add_argument('--sudo',           action='store_true', help="Use sudo to read configuration")
  parser.add_argument('--update-proxmox', action='store_true', help="Update Proxmox configuration")
  parser.add_argument('--update-dns',     action='store_true', help="Update DNS on Gandi")

  parser.add_argument('--vmid', action='store', type=int, help="Check specific vmid")
  args = parser.parse_args()

  return args


if __name__ == '__main__':
  args = parse_args()

  if args.update_dns and "GANDI_APIKEY" not in os.environ:
    print(colored("ERROR: please set $GANDI_APIKEY when updating DNS", "yellow"))
    sys.exit(1)

  cn = CheckNetwork(args.read_proxmox, args.update_proxmox, args.update_dns)

  cfg = cn.read_config(args.path, args.vmid, args.sudo)
  cn.check_config(args.vmid)

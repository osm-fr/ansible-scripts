#!/usr/bin/env python3

import requests


class GandiAPI:

  gandi_api_url = "https://api.gandi.net/v5/"

  def __init__(self, domain, api_key):
    self.domain = domain
    self.api_key = api_key
    self.sharing_id = None

    self.headers = {'authorization': 'Apikey ' + self.api_key}

    orgs = self.get_organizations()
    for org in orgs:
      self.sharing_id = org["id"]
      domains = self.get_domains()
      domain_index = next((index for (index, d) in enumerate(domains) if d["fqdn"] == domain), None)
      if domain_index is not None:
        break

    if domain_index is None:
        print("The requested domain " + domain + " was not found in this gandi account")
        exit(1)

    self.domain_records_href = domains[domain_index]["domain_records_href"]

  def get_domains(self):
    if self.sharing_id:
      response = requests.get(self.gandi_api_url + "livedns/domains?sharing_id=" + self.sharing_id, headers=self.headers)
    else:
      response = requests.get(self.gandi_api_url + "livedns/domains", headers=self.headers)
    if (response.ok):
      domains = response.json()
      return domains
    else:
      response.raise_for_status()
      exit(1)

  def get_organizations(self):
    response = requests.get(self.gandi_api_url + "organization/organizations", headers=self.headers)
    if (response.ok):
      orgs = response.json()
      return orgs
    else:
      response.raise_for_status()
      exit(1)

  def get_ipv6(self, hostname):
    # Get recorded IP
    response = requests.get(self.domain_records_href + "/" + hostname + "/AAAA?sharing_id=" + self.sharing_id, headers=self.headers)
    if (response.ok):
      record = response.json()
      return record
    else:
      print("Failed to look for recorded IP")
      response.raise_for_status()
      exit(1)

  def update_ipv6(self, hostname, ip):
    # Set recorded IP
    record = self.get_ipv6(hostname)
    if ip != record['rrset_values'][0]:
      record['rrset_values'][0] = ip
      response = requests.put(self.domain_records_href + "/" + hostname + "/AAAA", headers=self.headers, json=record)
      if (response.ok):
        record = response.json()
        return True
      else:
        print("Failed to look for recorded IP")
        response.raise_for_status()
        exit(1)
    return False

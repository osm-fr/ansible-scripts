overpass-api
============

This role install overpass-api and one script which will setup the database on first boot.

Requirements
------------

No special requirements; note that this role requires root access, so either run it in a playbook with a global become: yes, or invoke the role in your playbook.

Role Variables
--------------

```
user: overpass
overpass_version: skip
overpass_pbf_region: planet
overpass_pbf_root_url: https://planet.osm.org/pbf
overpass_replication_url: https://planet.osm.org/replication/minute
overpass_replication_interval: minute
```

`user` is the owner of the overpass database and files.

The `overpass_version` refer to version used in http://dev.overpass-api.de/releases/. For example, `v0.7.54`.

`overpass_replication_interval` can be `minute` or `day`.

Dependencies
------------

This role depends on `shared/project-account.yml`.

Example Playbook
----------------

```yaml
- name: overpass-api.yml
  hosts: overpass-api
  gather_facts: no
  roles:
    - role: overpass-api
      when: overpass_version != "skip"
      become: yes
```

# Ansible scripts to handle OSM-FR machines

This repository contains various scripts to setup and configure machines
handled by OSM-FR association (a french association for OpenStreetMap). These
scripts are used with [ansible](https://www.ansible.com/).

## Configuring ansible

A version of ansible >= 2.3 is sufficient, and is available in Debian,
or from [git repository](https://github.com/ansible/ansible.git). To install all
dependency on Debian, use:

  ```shell
  apt-get install ansible python-jmespath
  ```

To install VM through proxmox, python promoxer module is necessary, It can be
installed with:

  ```shell
  sudo pip install proxmoxer
  ```

## Using ansible scripts

### Installation and configuration of a new VM with proxmox

1. launch `./tools/add-vm.py` to update file `hosts` and create proxmox configuration. Command line options are available to change parameters like number of cpus or size of disk.
1. set shell variables `PROXMOX_PASSWORD` and `PROXMOX_SSHPUBKEY`
1. launch following command to create VM, configure network on host for ipv6 access, and update local `/etc/hosts` to access VM before DNS update:
    ```shell
    ansible-playbook -u root -l <hostname> common.yml
    ```

### Configuration of a new machine with default configuration

1. add the machine to file `hosts`, in section `[vm]` if it is a virtual machine, at the top otherwise.
1. launch following command:
    ```shell
    ansible-playbook -l <hostname> common.yml
    ```

### Adding a new user to a specific machine

1. add the machine to file `hosts`, in the relevant section `[user]`
1. if necessary, add the user to `roles/common/tasks/main.yml`, with the public ssh key in `public\_keys/<user>`
1. launch following command:
    ```shell
    ansible-playbook -l <hostname> common.yml --tags user_creation
    ```

### Adding a service to a specific machine

1. add the machine to file `hosts`, in the relevant section `[service]`
1. launch following command:
    ```shell
    ansible-playbook -l <hostname> <service>.yml
    ```

# Ansible scripts to handle OSM-FR machines

This repository contains various scripts to setup and configure machines
handled by OSM-FR association (a french association for OpenStreetMap). These
scripts are used with [ansible](https://www.ansible.com/).

## Installing dependencies

### Installing on Debian

A version of ansible >= 2.3 is sufficient, and is available in Debian,
or from [git repository](https://github.com/ansible/ansible.git). To install all
dependency on Debian, use:

  ```shell
  apt-get install ansible
  ```

To install VM through proxmox, python promoxer module is necessary, It can be
installed with:

  ```shell
  apt-get install python3-proxmoxer
  ```
  
### Installing using `venv`

`venv` module creates isolated Python environments.

First of all, install the required packages. On Debian, use:

  ```shell
  apt-get install python3 python3-venv
  ```

You can jump into a new isolated environments using:

  ```shell
  python3 -m venv <folder>      # Create the environment, only needs to be done once
  source <folder>/bin/activate  # Run a subshell using the environment 
  ```
  
Then, install the required packages:

  ```shell
  pip install -r requirements.txt
  ```

Note: The created environment folder should be placed outside this project folder to prevent `ansible-lint` from looking at it.

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
1. if necessary, add the user to `group_vars/all/accounts.yml`, with the public ssh key in `public\_keys/<user>`
1. launch following command:
    ```shell
    ansible-playbook -l <hostname> accounts.yml
    ```

### Adding a service to a specific machine

1. add the machine to file `hosts`, in the relevant section `[service]`
1. launch following command:
    ```shell
    ansible-playbook -l <hostname> <service>.yml
    ```

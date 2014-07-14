Ansible scripts to handle OSM-FR machines
=========================================

This repository contains various scripts to setup and configure machines
handled by OSM-FR association (a french association for OpenStreetMap). These
scripts are used with [ansible][http://www.ansibleworks.com/].


Configuring ansible
-------------------

A version of ansible >= 1.4 is sufficient, and is available in Debian testing,
or from git repository https://github.com/ansible/ansible.git


Then, a few variables are needed to launch ansible easily.

    source init.sh


Using ansible scripts
---------------------

* Configuration of a new machine with default configuration.
  1. add the machine to file **hosts**, in section [vm] if it is a virtual
machine, at the top otherwise.
  2. launch following command:
        ```
        ansible-playbook -l <hostname> common.yml
        ```

* Adding a new user to a specific machine.
  1. add the machine to file **hosts**, in the relevant section [*user*]
  2. if necessary, add the user to roles/common/tasks/main.yml, with the public
ssh key in public\_keys/<user>
  3. launch following command:
        ```
        ansible-playbook -l <hostname> common.yml --tags user_creation
        ```

* Adding a service to a specific machine.
  1. add the machine to file **hosts**, in the relevant section [*service*]
  2. launch following command:
        ```
        ansible-playbook -l <hostname> <service>.yml
        ```

# ansible-plugins

"Collection" of useful plugins. 

## Installing plugins
Within your ansible root directory, edit your ansible.cfg to point at the directory with plugins.
You can use relative paths!

### Example callback plugins:
``` 
# ansible.cfg
[defaults]
inventory=hosts
callback_whitelist = timer, debug_failure
callback_plugins = plugins/callback

[ssh_connection]
ssh_args=-o ForwardAgent=yes
```

## Plugins

### Callbacks
#### debug_failure 
- Outputs hostvar variables for a failed task, tasks information and host information. This is useful for finding what exact variables and state your task was in when it failed. 

Example playbook:
```
- name: Handle error
  hosts: local
  connection: local
  tasks:
  - name: set the application tag
    set_fact: ami_application_tag="{{ sub_domain }}-{{ domain | replace('.', '-') }}"
  - name: Handle the error
    block:
      - debug:
          msg: 'I execute normally'
      - name: i force a failure
        command: /bin/false
      - debug:
          msg: 'I never execute, due to the above task failing, :-('
    rescue:
      - debug:
          msg: 'I caught an error, can do stuff here to fix it, :-)'
```
Output:
```

TASK [i force a failure] *******************************************************************************************************************************
fatal: [localhost]: FAILED! => {"changed": false, "cmd": "/bin/false", "msg": "[Errno 2] No such file or directory: '/bin/false': '/bin/false'", "rc": 2}
*************************FAILURE VARIABLES*************************
ami_iam_role: ami
ami_to_load: base
apache_home_dir: /Users/slunn/work/infra/ansible/playbooks/../files/tmp/httpd-conf
application: dw-test
asg_desired_size: 1
asg_max_size: 4
asg_min_size: 1
aws_build: true
build_type: none
cidr_16: 172.24
cluster_build: aws
custom_ami: ami-4bf3d731 
elb_name:
gather_subset: ['all']
group_names: ['local']
home_directory: /home/${base.project.name}
instance_profile_name: images
instance_size: t2.medium
instance_spot_price: 0.05
inventory_dir: /Users/slunn/work/infra/ansible/hosts
inventory_file: /Users/slunn/work/infra/ansible/hosts/static
inventory_hostname: localhost
inventory_hostname_short: localhost
module_setup: True
mysql_use_ssl: True
playbook_dir: /Users/slunn/work/infra/ansible/playbooks
production_build: true
production_js_build: true
project_dir: /Users/slunn/work/infra/ansible/playbooks/..
project_folder: websites
region: us-east-1
remote_home_folder: /home/centos
server_environment: staging
server_iam_role: host-ami
shrink_db_connections: False
store_build_local_properties: False
sub_domain: dw-test
subnet_a_cidr: 172.24.1.0/24
subnet_c_cidr: 172.24.3.0/24
subnet_d_cidr: 172.24.4.0/24
subnet_e_cidr: 172.24.5.0/24
use_private_ip_ec2: False
use_prod_robots: False
vars_file: config/vars.qa.yml
volume_size: 8
*************************FAILURE HOST INFO*************************
Host information: {
    "group_names": [
        "local"
    ],
    "inventory_hostname": "localhost",
    "inventory_hostname_short": "localhost"
}

*************************FAILURE TASK INFO*************************
Task Name: i force a failure
Task information: {
    "_ansible_no_log": false,
    "_ansible_parsed": true,
    "changed": false,
    "cmd": "/bin/false",
    "invocation": {
        "module_args": {
            "_raw_params": "/bin/false",
            "_uses_shell": false,
            "argv": null,
            "chdir": null,
            "creates": null,
            "executable": null,
            "removes": null,
            "stdin": null,
            "warn": true
        }
    },
    "msg": "[Errno 2] No such file or directory: '/bin/false': '/bin/false'",
    "rc": 2
}
```

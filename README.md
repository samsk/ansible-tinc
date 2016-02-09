# Tinc

This playbook generates tinc config for whole tinc vpn network, and deploys configs to ssh reachable hosts.

## Running

Create a tinc hosts file.

```bash
$ cat /etc/tinc/hosts
[vpn1]
gw1	ansible_ssh_host=vpn-host1	tinc_ip=172.16.100.1	tinc_hostname=gw1.in.domaim
gw2	ansible_connection=local	tinc_ip=172.16.100.2	tinc_hostname=gw2.in.domain	tinc_remote=gw2.some-dynamic-dns.org tinc_subnet='["172.16.100.2/32","192.168.11.0/24"]'
gw3	ansible_ssh_host=vpn-host3	tinc_ip=172.16.100.18	tinc_hostname=gw3.in.domain	tinc_subnet='172.16.100.16/29' tinc_port=1655
client1	ansible_connection=local	tinc_ip=172.16.100.10	tinc_hostname=client1.in.domain
client2 ansible_connection=local	tinc_ip=172.16.100.11	tinc_hostname=client2.in.domaim os_family=Android tinc_connect='["gw1","gw2"]'
[vpn2]
...

```

Next up, run ansible.

```bash
$ ansible-playbook site.yml -e netname=vpn1
```

If that completes OK, all the hosts accessible via ssh (ansible_connection != local) will have tinc configured and running. All other hosts will have tinc configuration generated in config
directory, so it can be distributed manualy as necessary.
*If you want to auto setup tinc on local node, you can not configure it as ansible_connection=local, because this will not deploy generated scripts. But this will not slow down local script
generation, config for every node is first localy generated and only after that synchronized to remote node.*

## IP addressing

It is necessary to specify **tinc_ip** for each hosts in ansible hosts file. This ip will be then configured on hosts, and used for vpn routing. It is additionaly possible to override additional
subnets that are reachable via given hosts via **tinc_subnect**

## Config variables

- **tinc_ip**		- host internal vpn ip *required*
- **tinc_hostname**	- host internal hostname, used to generated internal hosta file and zone file (default = inventory_hostname)
- **tinc_remote**	- host remote address, if it is differs form ansible_ssh_host or is not reachable via ssh at all (default = ansible_ssh_host)
- **tinc_port**		- specify different port to listen to (default = 655)
- **tinc_subnet**	- subnets that should be assigned to given tinc host (default = tinc_ip/32)
- **tinc_compression**	- specify tinc compression level (default = 10)
- **tinc_indirect**	- set IndirectData (default = 'no')
- **tinc_connect**	- by default all hosts will connecti only to public hosts (where ansible_connection != local), with this you can override this list
- **os_family**		- override *ansible_os_family*, this is specially there for Android clients

## Custom Up/Down scripts

This playbook automatically generates tinc up/down scripts (like tinc-up, subnet-up etc...) that can be anytime regenerated. Therefore it is possible to setup on-site scripts that
will be automaticaly executed from [tinc up/down script](http://www.tinc-vpn.org/documentation/Scripts.html).
This scripts should reside in tinc parent directory (obviously /etc/tinc). This scripts will handle all tinc network actions.
To handle only one specific network, create them like *<script>.<netname>* (ie. /etc/tinc/tinc-up.vpn1).
Along with default [tinc script variables](http://www.tinc-vpn.org/documentation/Scripts.html) there are also few others provided (see /etc/tinc/*netname*/common.sh).

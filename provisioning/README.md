# ansible-tower - Provisioning

Infrastructure as Code

Go 0 - 100, bare metal to Infrastructure as a Service (Redhat Openstack Platform 10) using vlans for tenant segmenting, Application as a Service (Openshift Enterprise 3.5), over a hybrid cloud (Openstack and AWS deployments), with environment/server patch management with Redhat Insights, using Ansible Tower as a Role Based Infrastructure Configuration Manager.  DNS is automatically updated whenever a vm is spun up in openstack, aws, or an application is created in Openshift.

Takes one hour to install OSP 10 on 3 nodes (1 controller + compute node, 2 compute nodes), 30 mins to deploy Ansible Tower 3.3, 30 mins to deploy OSE 3.5.

TODO: Network Hardware (router and Switch) vlan configuration, dhcp and dns server configuration

NOTE: Check out NETWORK.md for network configuration

Requirements

- vlans created on router and switches
- two nics per servers
- first nic can pxe boot and optionally natively set to your vlan of choice on the switch, and second nic is trunked on switch
- server remote management/ipmi/idrac/ilo/etc is configured and works with linux ipmi utilities. Configured to use vlan 101
- dhcp server to manage pxe booting, with a dhcp update key set
- working dns server, and dhcp server can update dns records

This document has the following objectives:

- any server in vlan 101 can be remotely rebooted, and configured to reboot to pxe one time or the local disk permenantly.
- any server in vlan 102 can be provisioned remotely via dhcp and tftp
- using ansible, we provision and deploy a 3 node Openstack Cluster to provide Infrastructure as a Service
- using Openstack, we can provision a VM in any of the vlans on our switch
- Openstack VMs will have DNS entries automatically created and destroyed.
- we provision a vm, have it register to Redhat/Satellite, install our keys and MOTD, we test that its DNS entry works and we can access it
- using Openstack Cinder, we can provide Storage as a Service to containers
- we deploy Openshift OSE 3.5 to provide Software as a Service, using Openstack Cinder provided storage.
- Openshift Applications will have DNS entries automatically created and destroyed.
- we create an Openshift application and test that DNS works, it returns the expected content, and the persistent data is stored in the correct Cinder volume.
- we deploy Ansible Tower to manage the Infrastructure
- we patch the infrastructure
- we deploy into AWS to create a hybrid cloud.
- finally, we use Redhat Enterprise Linux 7 for this demonstration, but I wouldn't be a good engineer if I didn't abstract the code at the OS level. Not all of software used is available for other OS, but the code is reusable. A base is provided for Centos, Ubuntu, Fedora, and Atomic Linux for the reader's pleasure.


Update provisioning/group_vars/all with your specific configuration and passwords. You can encrypt and put your root passwords, aws secret keys, etc in this file

REQUIRED:
 - Your Redhat Customer Portal/Satellite username/password
 - Your subscription pool name or pool ids

 OPTIONAL:
 - Openstack Credentials
 - AWS Credentials
 - Private and Public Keys to place on servers


If you already have Ansible Tower set up, It's really easy:

Step 1: Create some new Credentials in Settings Gear
 - Rename 'Demo Credential' to Dummy Credential
 - 'RootPw' Choose Machine. Root username/password/ssh private key
 - 'Cloud User' Choose Machine. An unprivileged user, but in the wheel group, that is used for general ssh access
 - 'Redhat Lab Openstack Project' Openstack user/password/project to use. Change or add a couple as needed.
 - 'AWS Developer Account' Choose type AWS. Change the name as needed.  Aws ec2 access key and access secret
 - 'AWS SSH Key' Choose Machine. Use as needed.
 - 'Redhat Insights' - Choose Source Control, and enter your Redhat Customer Portal username
 - set a Vault password on each Credential, use the same password for each one

Step 2: Create some new Projects, 
 - 'Deployments' for quick ansible jobs,
 - 'Installations' for long running jobs, 
 - 'Patch Management' Choose Redhat Insights, and provide the Insights Credential to apply system patches
 - 'Developers' for a non privileged User Work Flows, ie they can't pxe boot the payroll files server. You can give them access to a specific Openstack Project Credential, or AWS account credential, for example.

Point all of the projects, except 'Patch Management', to this repo or another SCM repo you've committed this to.

	https://github.com/syspimp/ansible-tower.git

Step 3: Create some new Inventories
 - Rename 'Demo Inventory' to 'Localhost Inventory'
 - 'AWS Dev Account' - dynamic inventory, use the AWS cloud credential, create as many as needed to pull from AWS
 - 'Openstack' - dynamic inventory, use the Openstack cloud credential and it pulls from Openstack
 - 'Physical' - click add group, manual, and add the 3 physical servers IP here
 - 'Proof of Concept' - some other groups for you
 - 'Dev' - some other groups for you 
 - 'Staging' - some other groups for you 
 - 'Etc'

NOTE: The reason for so many groups is long running jobs lock the Ansible Tower Inventory and Code revisions for updates so while the one long job is running, subsequent job runs will not update the project code or nodes in that particular inventory (We will also create multiple inventories). This is not desirable in a devops/agile environment. The solution is create a project (and inventories) for long running tasks :) This lets you get on with your work while the long running tasks use what was available at the time of its launch without slowing down work flow.  Only the unique entries in the multiple inventories are counted towards your license.


Step 4: Create some Job Templates to do real work

Most of the work will be done in the ansible-tower/provisioning/ directory.

You can override the variables located in ansible-tower/provisioning/group_vars/all in the job template, or update the variables in the file itself. 


1. Power - Reboot into PXE (which will reinstall the OS, shutdown)
 - Choose Job Type Run
 - Localhost Inventory
 - Deployments Project
 - provisioning/control-rack-power.yml Playbook
 - Dummy Crendential (its run on localhost)

 In the Extra Variables section, enter the IPMI targets you want to control and the power state, or create a Survey that asks for it. In this example, we set 3 servers to boot to pxe (and reinstall because we configured them to reinstall in dhcp and tftp)

	---
	ipmi_targets:
	  - 10.55.101.158
	  - 10.55.101.157
	  - 10.55.101.156
	powerstate: "pxe"


2. Power - Off
Copy the Power - Reboot template and rename it to 'Power - Off'. Leave the settings the same, except use the following for extra variables:

Extra Variables:
	---
	ipmi_targets:
	  - 10.55.101.158
	powerstate: "off"

3. Power - On
You guessed it.

Extra Variables:
	---
	ipmi_targets:
	  - 10.55.101.158
	powerstate: "on"

Read the playbook for more power states.

## Openstack IaaS
1. Deploy OSP all-in-one on a single server
 - Choose Job Type Run
 - Physical Inventory
 - Deployments Project
 - provisioning/deploy-osp-10.yml Playbook
 - RootPw Credentials

This will power on the servers and include the firstboot.yml scripts, which register them to Redhat Subscription Manager, configure repos, configures the cloud-user account info (password, key, etc), root password, MOTD and a few other things before running the command packstack --allinone.

Read the group_vars/all file for all the variables you can set. You will definitely need your Redhat Customer Portal password set in this file, or in the Extra Variables section.  https://github.com/syspimp/ansible-tower/blob/master/provisioning/group_vars/all

Extra Variables:

	---
	# this includes the control-rack-power.yml playbook, so we set the targets here, too
	ipmi_targets:
	  - 10.55.101.158
	  - 10.55.101.157
	  - 10.55.101.156
	powerstate: "on"

	## this toggles all-in-one or using a packstack answer-file
	os_packstack_use_answerfile: "no"
	## override group_vars/all to fix compute nodes only getting base repos
	rh_enabled_repos: ['rhel-7-server-optional-rpms','rhel-7-server-rpms','rhel-7-server-extras-rpms','rhel-7-server-openstack-10-rpms','rhel-7-server-rh-common-rpms','rhel-7-server-extras-rpms','rhel-7-server-openstack-10-devtools-rpms']


2. Deploy OSP on several nodes

Same as above, except using an answer file and spread over 3 servers

	---
	ipmi_targets:
	  - 10.55.101.158
	  - 10.55.101.157
	  - 10.55.101.156
	powerstate: "on"

	## this toggles all-in-one or using an answer-file
	os_packstack_use_answerfile: "yes"
	## settings for the answer file
	os_controller_nodes: "{{ ansible_default_ipv4['address'] }}"
	os_compute_nodes: "{{ ansible_default_ipv4['address'] }},10.55.102.157,10.55.102.156"
	os_network_nodes: "{{ ansible_default_ipv4['address'] }}"
	os_amqp_nodes: "{{ ansible_default_ipv4['address'] }}"
	os_mariadb_nodes: "{{ ansible_default_ipv4['address'] }}"

	## fix for compute nodes only getting base repos
	rh_enabled_repos: ['rhel-7-server-optional-rpms','rhel-7-server-rpms','rhel-7-server-extras-rpms','rhel-7-server-openstack-10-rpms','rhel-7-server-rh-common-rpms','rhel-7-server-extras-rpms','rhel-7-server-openstack-10-devtools-rpms']

3. Customize OSP 10
 - Choose Job Type Run
 - Physical Inventory
 - Installations Project
 - provisioning/openstack-customize.yml Playbook
 - RootPw Credentials
 - Limit 10.55.102.158 (or whatever is your controller node)
 - Enable Privilege Escalation
 - Click Save

 This creates an Openstack project named Redhat_Lab, a user named 'dtaylor' and imports RHEL-7 cloud image, Atomic cloud image, and a PXE boot image. You will need to customize the user and glance images to import.



## General Provisioning Callback Job Templates
1. Firstboot for Openstack Callback Job Template
 - Choose Job Type Run
 - Openstack Inventory
 - Installations Project
 - provisioning/firstboot.yml Playbook
 - Cloud User Credentials
 - Openstack Cloud Credentials
 - Enable Privilege Escalation
 - Enable Provisioning Callbacks
 - Click Generate Host Config Key
 - Click Save

When a virtual server is provisioned, it can phone home to finish it's configuration. Ansible Tower will verify the calling server is in the inventory managed by the Job Template, and then run against the calling server. We use cloud-config to configure the virtual (openstack or aws or any other platform that support cloud-config) to phone home.

Make note of the Host Config Key and the Pop Up with info about the Host Config Key. You will need this Key and the Job ID later for Job Templates that call this job.

2. Security - Run Redhat Insight Patch Plans on Openstack RHEL VMs

You will need to log into https://access.redhat.com/insights, create and save a patching plan. Once created and called, the calling server will be patched/updated.

 - Choose Job Type Run
 - Openstack Inventory
 - Redhat Insights Project
 - provisioning/<your patching plan here>.yml Playbook
 - Cloud User Credentials
 - Openstack Cloud Credentials
 - Enable Privilege Escalation
 - Enable Provisioning Callbacks
 - Click Generate Host Config Key
 - Click Save

Remember the Host Config Key and Job ID for later (or come back and get it)


Steps 3 and 4:  Create firstboot and Insights plan for AWS VMs

Do the same as above, except choose AWS inventory and Cloud Credentials.


## Callbook Job Templates to install applications
2. Install Openshift 3.5 on Openstack
 - Choose Job Type Run
 - Openstack Inventory
 - Installations Project
 - provisioning/install-ose-3.5.yml Playbook
 - Cloud User Credentials
 - Enable Privilege Escalation
 - Enable Provisioning Callbacks
 - Click Generate Host Config Key
 - Click Save

This callback script is not run directly and non admin groups shouldn't have access to this for this demo. It should be called by a Deploy Job Template script that a non admin user has access to. It can be run directly, of course, if you set the limit properly or modify the playbook to apply to a selected host or group, otherwise it will run on all hosts in an inventory. This installs an Openshift Controller and node on a single VM. You can scale it out by running another Job Template

3. Provision Openshift 3.5 on Openstack
 - Choose Job Type Run
 - Openstack Inventory
 - Deployments Project
 - provisioning/launch-openstack-vm.yml Playbook
 - Dummy Credentials
 - Openstack Cloud Credentials

Extra Variables:
	---
	##  this says to create a cinder volume named 'ose-volume'. We use this for docker container persistent data
	os_create_volume: "yes"
	os_volume_size: 5
	os_volume_name: ose-volume
	os_server:
	  name: "RHEL OSE 3-5 Demo"
	  state: present
	  image: "RHEL 7.3 Cloud"
	  flavor: "m1.medium"
	  network: "Provisioning_102"
	  availability_zone: "nova"
	  region_name: "RegionOne"
	  auto_ip: no
	  key_name: "dtaylor-openstack"
	  
	## this calls the install ose playbook
	host_config_key: 0c4fbc7946308401af78735e800f45e3
	host_config_server: 10.55.102.248
	host_config_jobid: 139
	## this calls the redhat insights security patching playbook
	redhat_insights_key: 990c2493aefba904a89081496fc0319b
	redhat_insights_jobid: 117

1. Provision AWS Instance(s)
2. Provision Openshift 3.5 on AWS
3. Provision Ansible Tower on AWS


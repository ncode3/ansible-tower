#ansible-tower

Network Setup

PREWORK

Router configuration:

NOTE: This is provided for completeness. We only use vlan 101 and 102 for this demonstration. vlan 101 is to remotely boot the server via IPMI, vlan 102 is the where the server will pxeboot and general system management access will occur.  The ip-address line is the gateway that we will route as the default route for each subnet/vlan. Also note that the dhcp/dns server port allows the storage vlan, so it can mount whatever it needs off of the storage appliance.

	interface GigabitEthernet0/0.101
	 description IPMI Vlan 101
	 encapsulation dot1Q 101
	 ip address 10.55.101.1 255.255.255.0
	 ip pim dense-mode
	 ip flow ingress
	 ip nat inside
	 ip virtual-reassembly in
	 no cdp enable
	!
	interface GigabitEthernet0/0.102
	 description Provisioning Vlan 102
	 encapsulation dot1Q 102
	 ip address 10.55.102.1 255.255.255.0
	 ip pim dense-mode
	 ip flow ingress
	 ip nat inside
	 ip virtual-reassembly in
	 no cdp enable
	!
	interface GigabitEthernet0/0.103
	 description API Vlan 103
	 encapsulation dot1Q 103
	 ip address 10.55.103.1 255.255.255.0
	 ip pim dense-mode
	 ip flow ingress
	 ip nat inside
	 ip virtual-reassembly in
	 no cdp enable
	!
	interface GigabitEthernet0/0.104
	 description Tenant Vlan 104
	 encapsulation dot1Q 104
	 ip address 10.55.104.1 255.255.255.0
	 ip pim dense-mode
	 ip flow ingress
	 ip nat inside
	 ip virtual-reassembly in
	 no cdp enable
	!
	interface GigabitEthernet0/0.105
	 description Storage Vlan 105
	 encapsulation dot1Q 105
	 ip address 10.55.105.1 255.255.255.0
	 ip pim dense-mode
	 ip flow ingress
	 ip nat inside
	 ip virtual-reassembly in
	 no cdp enable
	!
	interface GigabitEthernet0/0.106
	 description Storage Mgmt Vlan 106
	 encapsulation dot1Q 106
	 ip address 10.55.106.1 255.255.255.0
	 ip pim dense-mode
	 ip flow ingress
	 ip nat inside
	 ip virtual-reassembly in
	 no cdp enable
	 !
	interface GigabitEthernet0/0.107
	 description External Vlan 107
	 encapsulation dot1Q 107
	 ip address 10.55.107.1 255.255.255.0
	 ip pim dense-mode
	 ip flow ingress
	 ip nat inside
	 ip virtual-reassembly in
	 no cdp enable
	!
	interface GigabitEthernet0/0.108
	 description Float IP Vlan 108
	 encapsulation dot1Q 108
	 ip address 10.55.108.1 255.255.255.0
	 ip pim dense-mode
	 ip flow ingress
	 ip nat inside
	 ip virtual-reassembly in
	 no cdp enable
	!

Switch Configuration for server nics em1 enp10s0f1 and the dhcp/dns server:

	interface GigabitEthernet0/2
	 description compute2 em1 10.55.102.156 trunked native vlan102
	 switchport trunk encapsulation dot1q
	 switchport trunk native vlan 102
	 switchport trunk allowed vlan 101,102
	 switchport mode trunk
	!
	interface GigabitEthernet0/3
	 description compute3 em1 10.55.102.157 trunked native 1vlan02
	 switchport trunk encapsulation dot1q
	 switchport trunk native vlan 102
	 switchport trunk allowed vlan 101,102
	 switchport mode trunk
	!
	interface GigabitEthernet0/4
	 description compute4 em1 10.55.102.158 trunked native vlan102
	 switchport trunk encapsulation dot1q
	 switchport trunk native vlan 102
	 switchport trunk allowed vlan 101,102
	 switchport mode trunk
	!
	! some skipped
	! this is the dns/dhcp server
	interface GigabitEthernet0/6
	 description dhcp and dns services 10.55.102.5 native vlan102
	 switchport trunk encapsulation dot1q
	 switchport trunk native vlan 102
	 switchport trunk allowed vlan 102,105
	 switchport mode trunk
	!
	! these are the nics the Openstack VM traffic will traverse
	interface GigabitEthernet0/16
	 description compute2 enp10s0f1 trunk
	 switchport trunk encapsulation dot1q
	 switchport mode trunk
	!
	interface GigabitEthernet0/18
	 description compute3 enp10s0f1 trunked
	 switchport trunk encapsulation dot1q
	 switchport mode trunk
	!
	interface GigabitEthernet0/20
	 description compute4 enp10s0f1 trunked
	 switchport trunk encapsulation dot1q
	 switchport mode trunk
	!
	! some skipped
	! these are the vlan interfaces, notice the no shut command to bring them up
	interface Vlan101
	 description IPMI vlan 101
	 ip address 10.55.101.3 255.255.255.0
	 no shutdown
	!
	interface Vlan102
	 description Provisioning vlan 102
	 ip address 10.55.102.3 255.255.255.0
	 no shutdown
	!
	interface Vlan103
	 description API vlan 103
	 ip address 10.55.103.3 255.255.255.0
	 no shutdown
	!
	interface Vlan104
	 description Tenant vlan 104
	 ip address 10.55.104.3 255.255.255.0
	 no shutdown
	!
	interface Vlan105
	 description Storage vlan 105
	 ip address 10.55.105.3 255.255.255.0
	 no shutdown
	!
	interface Vlan106
	 description Storage Mgmt vlan 106
	 ip address 10.55.106.3 255.255.255.0
	 no shutdown
	!
	interface Vlan107
	 description External vlan 107
	 ip address 10.55.107.3 255.255.255.0
	 no shutdown
	!
	interface Vlan108
	 description Floating IP vlan 108
	 ip address 10.55.108.3 255.255.255.0
	 no shutdown
	!

Code Snippets for how your dhcp and dns server configuration should look like. This is not a complete file:

dhcp snippets for host 10.55.102.5:

/etc/dhcp/dhcpd.conf:
	key dhcpupdate {
	  algorithm hmac-md5;
	  secret xxxxxxxxxxxx;
	};

	## some skipped
	zone redhat-lab.local {
	  primary 10.55.102.5;
	  key dhcpupdate;
	}
	## some skipped
	option domain-name "redhat-lab.local";
	ddns-domainname "redhat-lab.local";
	option domain-name-servers 10.55.102.5;
	option ntp-servers 10.55.102.5;
	next-server 10.55.102.5;
	filename "pxelinux.0";
	## some skipped
	subnet 10.55.102.0 netmask 255.255.255.0 {
	  pool
	  {
	    range 10.55.102.15 10.55.102.125;
	  }

	  option subnet-mask 255.255.255.0;
	  option routers 10.55.102.1;
	}
	## some skipped
	host compute2 {
	option host-name "compute2.redhat-lab.local";
	hardware ethernet 0:1d:09:xxxx;
	fixed-address 10.55.102.156;
	ddns-hostname "compute2";
	filename "reinstall/pxelinux.0";
	}
	host compute3 {
	option host-name "compute3.redhat-lab.local";
	hardware ethernet 0:21:9b:xxxx;
	fixed-address 10.55.102.157;
	ddns-hostname "compute3";
	filename "reinstall/pxelinux.0";
	}
	host compute4 {
	option host-name "compute4.redhat-lab.local";
	hardware ethernet 0:15:c5:xxxx;
	fixed-address 10.55.102.158;
	ddns-hostname "compute4";
	filename "reinstall/pxelinux.0";
	}

dns/bind 9 configuration for host 10.55.102.5:

/etc/named.conf:

	acl "trusted" {
	     10.55.0.0/16;
	     10.55.102.0/24;
	     localhost;
	     localnets;
	 };
	...
	include "/etc/named.conf.dhcp";

/etc/named.conf.dhcp:

key dhcpupdate {
  algorithm hmac-md5;
  secret "xxxxxxxxxxx";
};
zone "redhat-lab.local" {
  type master;
  file "dhcp/redhat-lab.local.zone";
  allow-update { key dhcpupdate; };
  allow-transfer { 10.55.0.0/16; localhost; ::1; };
};
zone "ose.redhat-lab.local" {
  type master;
  file "dhcp/ose.redhat-lab.local.zone";
  allow-update { key dhcpupdate; };
  allow-transfer { 10.55.0.0/16; localhost; ::1; };
};
zone "stack.redhat-lab.local" {
  type master;
  file "dhcp/stack.redhat-lab.local.zone";
  allow-update { key dhcpupdate; };
  allow-transfer { 10.55.0.0/16; localhost; ::1; };
};

NOTE: setting up your zone files is beyond the scope of this write-up, but here is a base you can start with. You need one for each zone you gave in /etc/named/named.conf:

/var/named/dhcp/ose.redhat-lab.local.zone:

	$ORIGIN .
	$TTL 300        ; 5 minutes
	ose.redhat-lab.local    IN SOA  redhat-lab.local. root.redhat-lab.local. (
	                                201613611  ; serial
	                                28800      ; refresh (8 hours)
	                                7200       ; retry (2 hours)
	                                604800     ; expire (1 week)
	                                86400      ; minimum (1 day)
	                                )
	                        NS      ns.redhat-lab.local.
	                        A       10.55.102.5
	$ORIGIN ose.redhat-lab.local.
	*                       CNAME   ose.redhat-lab.local.

Tftpboot configuration:

You need a default pxe boot menu option the times out to boot to local disk, and a menu option for an unattended system reinstall. You will provide the kickstart file. For now, this is beyond the scope to configure.



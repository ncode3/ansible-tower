```shell
[root@rhel-7-vm leap_second]# ansible-playbook -i all site.yml 

PLAY [all] *********************************************************************

TASK [setup] *******************************************************************
ok: [10.55.105.11]
ok: [10.55.3.153]
ok: [10.55.3.152]
ok: [10.55.3.151]
ok: [10.55.3.155]
ok: [10.1.10.10]
ok: [10.55.2.155]

TASK [leap_second : copying test script to host] *******************************
ok: [10.55.105.11]
ok: [10.55.3.153]
ok: [10.55.3.155]
ok: [10.55.3.152]
ok: [10.55.3.151]
ok: [10.55.2.155]
ok: [10.1.10.10]

TASK [leap_second : running leap second issue detector] ************************
changed: [10.55.105.11]
changed: [10.55.2.155]
changed: [10.55.3.153]
changed: [10.55.3.152]
changed: [10.55.3.155]
changed: [10.1.10.10]
changed: [10.55.3.151]

TASK [leap_second : check if need to update kernel] ****************************
skipping: [10.55.3.153]
skipping: [10.55.3.152]
skipping: [10.55.2.155]
skipping: [10.1.10.10]
changed: [10.55.105.11]
changed: [10.55.3.155]
changed: [10.55.3.151]

TASK [leap_second : check if need to update ntp] *******************************
skipping: [10.55.3.151]
skipping: [10.55.3.152]
skipping: [10.55.3.153]
skipping: [10.55.3.155]
skipping: [10.55.2.155]
skipping: [10.1.10.10]
changed: [10.55.105.11]

TASK [leap_second : forced failure when SUGGESTION detected] *******************
skipping: [10.55.3.153]
skipping: [10.55.3.152]
skipping: [10.55.2.155]
skipping: [10.1.10.10]
changed: [10.55.105.11]
changed: [10.55.3.155]
changed: [10.55.3.151]

TASK [leap_second : announce our results for logging] **************************
ok: [10.55.3.152] => {
    "msg": "\u001b[34m[INFORMATION]\u001b(B\u001b[m\n- Installed kernel version: 3.19.8-100.fc20.x86_64\n- The system is running NTP: ntp-4.2.6p5-22.fc20.x86_64\nWhen the leap second occurs, this systems time will be stepped by the kernel. Thus, it is configured to stay in sync with the true/official time.\n\nIf you would like to learn more on how to resolve Leap Second Issues in Red Hat Enterprise Linux, refer to <https://access.redhat.com/articles/15145>."
}
ok: [10.55.3.155] => {
    "msg": "\u001b[34m[INFORMATION]\u001b(B\u001b[m\n- Installed kernel version: 2.6.32-504.16.2.el6.x86_64\n- The system is running NTP: ntp-4.2.6p5-3.el6.centos.x86_64\nWhen the leap second occurs, this systems time will be stepped by the kernel. Thus, it is configured to stay in sync with the true/official time.\n\u001b[34m[SUGGESTIONS ON KERNEL]\u001b(B\u001b[m\nA known issue of kernel is detected and listed below. Refer to the link attached for the remediation steps.\n- Absolute timers may fire early when the leap second is inserted; this issue is documented in <https://access.redhat.com/solutions/1471933>.\n\nIf you would like to learn more on how to resolve Leap Second Issues in Red Hat Enterprise Linux, refer to <https://access.redhat.com/articles/15145>."
}
ok: [10.55.3.153] => {
    "msg": "\u001b[34m[INFORMATION]\u001b(B\u001b[m\n- Installed kernel version: 3.19.8-100.fc20.x86_64\n- The system is running NTP: ntp-4.2.6p5-22.fc20.x86_64\nWhen the leap second occurs, this systems time will be stepped by the kernel. Thus, it is configured to stay in sync with the true/official time.\n\nIf you would like to learn more on how to resolve Leap Second Issues in Red Hat Enterprise Linux, refer to <https://access.redhat.com/articles/15145>."
}
ok: [10.55.3.151] => {
    "msg": "\u001b[34m[INFORMATION]\u001b(B\u001b[m\n- Installed kernel version: 2.6.32-431.17.1.el6.x86_64\n- The system is running NTP: ntp-4.2.6p5-3.el6.centos.x86_64\nWhen the leap second occurs, this systems time will be stepped by the kernel. Thus, it is configured to stay in sync with the true/official time.\n\u001b[34m[SUGGESTIONS ON KERNEL]\u001b(B\u001b[m\nA known issue of kernel is detected and listed below. Refer to the link attached for the remediation steps.\n- Absolute timers may fire early when the leap second is inserted; this issue is documented in <https://access.redhat.com/solutions/1471933>.\n\nIf you would like to learn more on how to resolve Leap Second Issues in Red Hat Enterprise Linux, refer to <https://access.redhat.com/articles/15145>."
}
ok: [10.55.2.155] => {
    "msg": "\u001b[34m[INFORMATION]\u001b(B\u001b[m\n- Installed kernel version: 3.19.8-100.fc20.x86_64\n- The system is running NTP: ntp-4.2.6p5-22.fc20.x86_64\nWhen the leap second occurs, this systems time will be stepped by the kernel. Thus, it is configured to stay in sync with the true/official time.\n\nIf you would like to learn more on how to resolve Leap Second Issues in Red Hat Enterprise Linux, refer to <https://access.redhat.com/articles/15145>."
}
ok: [10.55.105.11] => {
    "msg": "\u001b[34m[INFORMATION]\u001b(B\u001b[m\n- Installed kernel version: 3.10.0-327.22.2.el7.x86_64\n- The system is running NTP: ntp-4.2.6p5-22.el7_2.2.x86_64\nWhen the leap second occurs, this systems time will be stepped by the kernel. Thus, it is configured to stay in sync with the true/official time.\n\u001b[34m[SUGGESTIONS ON KERNEL]\u001b(B\u001b[m\nA known issue of kernel is detected and listed below. Refer to the link attached for the remediation steps.\n- There is a chance that hrtimers may fire early when the leap second is inserted; this issue is documented in <https://access.redhat.com/solutions/2766351>.\n\u001b[34m[SUGGESTIONS ON NTP]\u001b(B\u001b[m\nA known issue of ntp is detected and listed below. Refer to the link attached for the remediation steps.\n- The ntpd leap status is not reset after inserting a leap second. Refer to <https://access.redhat.com/solutions/1530053> for more details.\n\nIf you would like to learn more on how to resolve Leap Second Issues in Red Hat Enterprise Linux, refer to <https://access.redhat.com/articles/15145>."
}
ok: [10.1.10.10] => {
    "msg": "\u001b[34m[INFORMATION]\u001b(B\u001b[m\n- Installed kernel version: 4.8.8-200.fc24.i686+PAE\n- The system is running NTP: ntp-4.2.6p5-41.fc24.i686\nWhen the leap second occurs, this systems time will be stepped by the kernel. Thus, it is configured to stay in sync with the true/official time.\n\nIf you would like to learn more on how to resolve Leap Second Issues in Red Hat Enterprise Linux, refer to <https://access.redhat.com/articles/15145>."
}

RUNNING HANDLER [leap_second : update kernel] **********************************
ok: [10.55.105.11] => {
    "msg": "You should run the fix_kernel playbook on this host 'rhstorage1"
}
ok: [10.55.3.151] => {
    "msg": "You should run the fix_kernel playbook on this host 'zenoss"
}
ok: [10.55.3.155] => {
    "msg": "You should run the fix_kernel playbook on this host 'public-web"
}

RUNNING HANDLER [leap_second : update ntp] *************************************
ok: [10.55.105.11] => {
    "msg": "You should run the 'ansible-playbook fix_ntp playbook on this host 'rhstorage1'"
}

RUNNING HANDLER [leap_second : forced failure] *********************************
fatal: [10.55.105.11]: FAILED! => {"changed": true, "cmd": "/bin/false", "delta": "0:00:00.004668", "end": "2016-12-12 20:10:36.974522", "failed": true, "rc": 1, "start": "2016-12-12 20:10:36.969854", "stderr": "", "stdout": "", "stdout_lines": [], "warnings": []}
fatal: [10.55.3.155]: FAILED! => {"changed": true, "cmd": "/bin/false", "delta": "0:00:00.017545", "end": "2016-12-12 20:10:37.131960", "failed": true, "rc": 1, "start": "2016-12-12 20:10:37.114415", "stderr": "", "stdout": "", "stdout_lines": [], "warnings": []}
fatal: [10.55.3.151]: FAILED! => {"changed": true, "cmd": "/bin/false", "delta": "0:00:00.021746", "end": "2016-12-12 20:10:38.135396", "failed": true, "rc": 1, "start": "2016-12-12 20:10:38.113650", "stderr": "", "stdout": "", "stdout_lines": [], "warnings": []}

NO MORE HOSTS LEFT *************************************************************
	to retry, use: --limit @site.retry

PLAY RECAP *********************************************************************
10.1.10.10                 : ok=4    changed=1    unreachable=0    failed=0   
10.55.105.11               : ok=9    changed=4    unreachable=0    failed=1   
10.55.2.155                : ok=4    changed=1    unreachable=0    failed=0   
10.55.3.151                : ok=7    changed=3    unreachable=0    failed=1   
10.55.3.152                : ok=4    changed=1    unreachable=0    failed=0   
10.55.3.153                : ok=4    changed=1    unreachable=0    failed=0   
10.55.3.155                : ok=7    changed=3    unreachable=0    failed=1   

[root@rhel-7-vm leap_second]# ansible-playbook -i all --limit @site.retry fix_kernel.yml

PLAY [all] *********************************************************************

TASK [setup] *******************************************************************
ok: [10.55.105.11]
ok: [10.55.3.155]
ok: [10.55.3.151]

TASK [fix_kernel_leap_second : make sure lsb rpm is installed, it helps for shell vars] ***
ok: [10.55.3.155]
ok: [10.55.3.151]
ok: [10.55.105.11]

TASK [fix_kernel_leap_second : check the os ver] *******************************
changed: [10.55.105.11]
changed: [10.55.3.155]
changed: [10.55.3.151]

TASK [fix_kernel_leap_second : output the os ver] ******************************
ok: [10.55.3.151] => {
    "msg": "CentOS 6"
}
ok: [10.55.3.155] => {
    "msg": "CentOS 6"
}
ok: [10.55.105.11] => {
    "msg": "RedHatEnterpriseServer 7"
}

TASK [fix_kernel_leap_second : update tzdata rpm] ******************************
ok: [10.55.3.151]
ok: [10.55.3.155]
ok: [10.55.105.11]

TASK [fix_kernel_leap_second : configure timezone for os when rhel version less than 7] ***
skipping: [10.55.105.11]
ok: [10.55.3.155]
ok: [10.55.3.151]

TASK [fix_kernel_leap_second : run tzdata-update when rhel version less than 7] 
skipping: [10.55.105.11]
changed: [10.55.3.155]
changed: [10.55.3.151]

TASK [fix_kernel_leap_second : configure timezone for os when rhel version 7 or Fedora] ***
skipping: [10.55.3.155]
skipping: [10.55.3.151]
changed: [10.55.105.11]

TASK [fix_kernel_leap_second : make sure kernel rpm is up to date] *************
ok: [10.55.3.151]
ok: [10.55.3.155]
changed: [10.55.105.11]

TASK [fix_kernel_leap_second : check the current date and time] ****************
changed: [10.55.105.11]
changed: [10.55.3.155]
changed: [10.55.3.151]

TASK [fix_kernel_leap_second : output the current time] ************************
ok: [10.55.105.11] => {
    "msg": "Mon Dec 12 20:15:58 EST 2016"
}
ok: [10.55.3.151] => {
    "msg": "Mon Dec 12 20:15:59 EST 2016"
}
ok: [10.55.3.155] => {
    "msg": "Mon Dec 12 20:15:58 EST 2016"
}

TASK [fix_kernel_leap_second : you should reboot] ******************************
ok: [10.55.3.151] => {
    "msg": "You should reboot this host zenoss"
}
ok: [10.55.105.11] => {
    "msg": "You should reboot this host rhstorage1"
}
ok: [10.55.3.155] => {
    "msg": "You should reboot this host public-web"
}

PLAY RECAP *********************************************************************
10.55.105.11               : ok=10   changed=4    unreachable=0    failed=0   
10.55.3.151                : ok=11   changed=3    unreachable=0    failed=0   
10.55.3.155                : ok=11   changed=3    unreachable=0    failed=0   

[root@rhel-7-vm leap_second]# ansible-playbook -i all --limit @site.retry fix_ntp.yml

PLAY [all] *********************************************************************

TASK [setup] *******************************************************************
ok: [10.55.105.11]
ok: [10.55.3.155]
ok: [10.55.3.151]

TASK [fix_ntp_leap_second : make sure lsb rpm is installed, it helps for shell vars] ***
ok: [10.55.3.151]
ok: [10.55.3.155]
ok: [10.55.105.11]

TASK [fix_ntp_leap_second : check the os ver] **********************************
changed: [10.55.105.11]
changed: [10.55.3.155]
changed: [10.55.3.151]

TASK [fix_ntp_leap_second : output the os ver] *********************************
ok: [10.55.105.11] => {
    "msg": "RedHatEnterpriseServer 7"
}
ok: [10.55.3.155] => {
    "msg": "CentOS 6"
}
ok: [10.55.3.151] => {
    "msg": "CentOS 6"
}

TASK [fix_ntp_leap_second : update tzdata rpm] *********************************
ok: [10.55.3.151]
ok: [10.55.3.155]
ok: [10.55.105.11]

TASK [fix_ntp_leap_second : configure timezone for os when rhel version less than 7] ***
skipping: [10.55.105.11]
ok: [10.55.3.155]
ok: [10.55.3.151]

TASK [fix_ntp_leap_second : run tzdata-update when rhel version less than 7] ***
skipping: [10.55.105.11]
changed: [10.55.3.155]
changed: [10.55.3.151]

TASK [fix_ntp_leap_second : configure timezone for os when rhel version 7 or Fedora] ***
skipping: [10.55.3.155]
skipping: [10.55.3.151]
changed: [10.55.105.11]

TASK [fix_ntp_leap_second : make sure ntp rpm is up to date] *******************
changed: [10.55.3.151]
changed: [10.55.3.155]
changed: [10.55.105.11]

TASK [fix_ntp_leap_second : check the current date and time] *******************
changed: [10.55.105.11]
changed: [10.55.3.155]
changed: [10.55.3.151]

TASK [fix_ntp_leap_second : output the current time] ***************************
ok: [10.55.3.151] => {
    "msg": "Mon Dec 12 20:19:05 EST 2016"
}
ok: [10.55.3.155] => {
    "msg": "Mon Dec 12 20:19:04 EST 2016"
}
ok: [10.55.105.11] => {
    "msg": "Mon Dec 12 20:19:04 EST 2016"
}

TASK [fix_ntp_leap_second : you should reboot] *********************************
ok: [10.55.3.151] => {
    "msg": "You should reboot this host zenoss"
}
ok: [10.55.3.155] => {
    "msg": "You should reboot this host public-web"
}
ok: [10.55.105.11] => {
    "msg": "You should reboot this host rhstorage1"
}

PLAY RECAP *********************************************************************
10.55.105.11               : ok=10   changed=4    unreachable=0    failed=0   
10.55.3.151                : ok=11   changed=4    unreachable=0    failed=0   
10.55.3.155                : ok=11   changed=4    unreachable=0    failed=0   

[root@rhel-7-vm leap_second]#
```

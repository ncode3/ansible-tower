#!/bin/bash
force=$1
days_to_keep=0
# make sure ansible is in a good state
ansible-tower-service restart
sleep 3
ansible-tower-service status > /dev/null

if [[ $? -ne 0 && "${force}" != '-f' ]]
then
  echo "Ansible Tower is not in a good state"
  echo "Use $0 -f to force"
  exit 1
fi

# remove all of the pending jobs
awx-manage shell_plus <<EOF
from awx.main.models import UnifiedJob
for i in UnifiedJob.objects.filter():
   if(i.status == 'pending'):
     i.delete()

EOF
# cleanup the old jobs
awx-manage cleanup_jobs --days=${days_to_keep}
awx-manage cleanup_activitystream --days=${days_to_keep}

# restart one last time
ansible-tower-service restart
sleep 3
ansible-tower-service status > /dev/null

if [[ $? -eq 0 ]]
then
  echo "Ansible Tower is good to go."
else
  echo "Error detected in ansible-tower-service status. Check the logs"
fi


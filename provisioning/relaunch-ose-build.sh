pass=ansible
id=258
if [ ! -z "$1" ]
then
  id="$1"
fi
echo "OSE 3.5 launch job ${id}"
curl -f -k -H 'Content-Type: application/json' -XPOST --user admin:${pass} https://10.55.102.248:443/api/v1/job_templates/${id}/launch/

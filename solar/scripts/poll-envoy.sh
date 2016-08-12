#!/bin/bash
tmpfile="/tmp/$$.solarpoll"
curl -s http://10.55.2.179/production?locale=en | grep Currently > $tmpfile
python parse-envoy.py $tmpfile
rm -f $tmpfile

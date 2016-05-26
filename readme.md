sudo docker pull centos

sudo docker run --privileged -p 8083:8083 -p 8086:8086 --name influxdb -id centos
sudo docker exec -it influxdb bash
yum install wget pycrypto -y
cd

wget https://bootstrap.pypa.io/get-pip.py
python get-pip.py
pip install Fabric
pip install influxdb

wget http://s3.amazonaws.com/influxdb/influxdb-0.8.8-1.x86_64.rpm
rpm -ivh influxdb-0.8.8-1.x86_64.rpm
/etc/init.d/influxdb start
influx --execute 'create database "dimensions"'


# vi fabfile.py
```
#!/usr/bin/env python
# -*- coding: utf-8 -*-

from fabric.api import local, put
from influxdb.influxdb08 import InfluxDBClient
import re

client = InfluxDBClient('localhost', 8086, 'root', 'root', 'dimensions')

def create_db():
    client.create_database('dimensions')

def loadaverage():
    out = local("uptime", capture=True)
    #print out
    match = re.search(r"load averages?:\s+(\d+\.\d+),\s+(\d+\.\d+),\s+(\d+\.\d+)", out)
    min1  = float(match.group(1))
    min5  = float(match.group(2))
    min15 = float(match.group(3))
    client.write_points([
        {
            "name": "loadaverage_1min",
            "columns": ["value"],
            "points": [[min1]]
        },
        {
            "name": "loadaverage_5min",
            "columns": ["value"],
            "points": [[min5]]
        },
        {
            "name": "loadaverage_15min",
            "columns": ["value"],
            "points": [[min15]]
        }
    ])
```
# exit

$ sudo docker run --privileged -p 3000:3000 --name grafana -id centos
$ sudo docker exec -it grafana bash
# yum install wget -y
# yum install initscripts fontconfig -y
# cd
# wget https://grafanarel.s3.amazonaws.com/builds/grafana-2.0.2-1.x86_64.rpm
# rpm -ivh grafana-2.0.2-1.x86_64.rpm
# /etc/init.d/grafana-server start


$ sudo docker run --privileged --name collector -id centos
$ sudo docker exec -it collector bash
# yum install wget pycrypto -y
# wget https://bootstrap.pypa.io/get-pip.py


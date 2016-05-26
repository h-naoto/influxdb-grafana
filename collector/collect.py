from fabric.api import local
from influxdb import InfluxDBClient
import re
import time


def generate_data():
    out = local("uptime", capture=True)
    match = re.search(r"load averages?:\s+(\d+\.\d+),\s+(\d+\.\d+),\s+(\d+\.\d+)", out)
    min1  = float(match.group(1))
    min5  = float(match.group(2))
    min15 = float(match.group(3))

    json_body = [
        {
            "measurement": "loadaverage_1min",
            "fields": {
                "value": min1
            }
        },
        {
            "measurement": "loadaverage_5min",
            "fields": {
                "value": min5
            }
        },
        {
            "measurement": "loadaverage_15min",
            "fields": {
                "value": min15
            }
        }
    ]
    return json_body


def create_db(client, name):
    print("create database:" + name)
    client.create_database(name)


def create_pol(client):
    print("Create a retention policy")
    client.create_retention_policy('awesome_policy', '3d', 1, default=True)


def write_point(client):
    data = generate_data()
    print("Write points: {0}".format(data))
    client.write_points(data)


def main():
    host = '192.168.56.101'
    port = '8086'
    user = 'root'
    password = 'root'
    dbname = 'dimensions'

    time.sleep(10)


    client = InfluxDBClient(host, port, user, password, dbname)
    create_db(client, dbname)
    create_pol(client)
    for var in range(0, 3600):
        write_point(client)
        time.sleep(1)


if __name__ == '__main__':
    main()

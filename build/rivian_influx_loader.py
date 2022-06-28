from RivianAPI import RivianAPI
import os
import time
import datetime

VEHICLE_ID      = os.environ.get("RIVIAN_VEHICLE_ID")
USERNAME        = os.environ.get("RIVIAN_USERNAME")
PASSWORD        = os.environ.get("RIVIAN_PASSWORD")
INFLUX_TOKEN    = "yyGao5gxwo6SuaVRlcYS58VuJYIe9Y7hIeYl2McAZQUHhOJmhS_CFLYqSg7lW0LQbcsicGSa5s9jsjsJaiM8ZQ=="
INFLUX_ORG      = "default"
INFLUX_BUCKET   = "rivian_data"

rivian = RivianAPI(VEHICLE_ID, USERNAME, PASSWORD)

from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS
from datetime import datetime

influx_client = InfluxDBClient(url="http://rivian-influxdb:8086", token=INFLUX_TOKEN, org=INFLUX_ORG)

def do_influx_update():
    write_api = influx_client.write_api(write_options=SYNCHRONOUS)
    #https://thenewstack.io/getting-started-with-python-and-influxdb/

    data = rivian.get_new_data()

    write_api.write(INFLUX_BUCKET, INFLUX_ORG, data, write_precision=WritePrecision.MS)


while True:
    time.sleep(5)
    do_influx_update()
    print(f'Polled at {datetime.now()}', flush=True)

import datetime

import influxdb_client
from influxdb_client.client.write_api import SYNCHRONOUS
from models import *

bucket = "deepak_portfolio"
org = "0d4e29f1e759c560"
token = "utKgzTWU1IRrbUzBHKu04CMraSMXZjQVVovDX21z1Gpne0aw2dM5MlJA2Hk0rO2C1N70WRTpOK8RkcAsUnJ0HQ=="
url = "http://localhost:8086"


def get_influxdb_connection():
    return influxdb_client.InfluxDBClient(
        url=url,
        token=token,
        org=org
    )

def writing_metrics_into_db(metrics, date):
    client = get_influxdb_connection()
    write_api = client.write_api(write_options=SYNCHRONOUS)
    p = influxdb_client.Point("myi_measurement")

    for metric in metrics.values():
        (p.field("Metric name", metric.name)
         .field("Money invested", metric.invested_amt)
         .field("Current value", metric.curr_amt)
         .field("Current gains (%)", metric.gains_percent)
         .time(date)
         )

    write_api.write(bucket=bucket, org=org, record=p)


metrics ={
    "New Metric": Metric("New Metric")
}

date = datetime.datetime(2024, 6, 10, 23, 0, 0, 123456).timestamp()
date = int(date) * 1000000000
# utctime = date.astimezone().ti
# date.n
# date = date.strftime("%Y-%m-%d")


writing_metrics_into_db(metrics, date)


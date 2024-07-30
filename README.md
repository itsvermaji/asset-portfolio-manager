## Key points to note
1. On a particular date, the portfolio value (sum of all the existing shares) is only calculated, if all the shares present in the portfolio have their share price data.

### Starting grafana on local

```bash
docker run \
    -p 8086:8086 \
    -v "$PWD/data:/var/lib/influxdb2" \
    -v "$PWD/config:/etc/influxdb2" \
    influxdb:2
```
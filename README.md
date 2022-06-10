# Guacamole Metrics Exporter for Prometheus

Export basic Apache Guacamole metrics to Prometheus.

Intended to be run in a container and based on API documentation from https://github.com/ridvanaltun/guacamole-rest-api-documentation, this will export the following for Prometheus

- The number of users in the database.
- The number of connections in the database.
- The number of active connections. <br>

![Alt text](https://github.com/freeflychi/guacamole-metrics-exporter/blob/main/metrics.png "Metrics in _Grafana_")

<br><br>

## Environment Variables

---

The following env vars are required

- `GUACAMOLE_HOST="guacamole.domain.com"`

- `GUACAMOLE_USER="guacadmin"` (a local, not LDAP user, with admin rights, e.g _guacadmin_)

- `GUACAMOLE_PASS="password"`

The following env vars is optional

- `SUPPRESS_SSL_WARNING="y"` (if guacamole is using an self-signed cert this will suppress the warning in the logs) <br><br>

## Build

---

`docker build -t guac-metrics-exporter -f Dockerfile.metrics .` <br><br>

## Run

---

```
docker run -d -p 8000:8000 -e GUACAMOLE_HOST="guacamole.domain.com" \
    -e GUACAMOLE_USER="guacadmin" \
    -e GUACAMOLE_PASS="password" \
    -e SUPPRESS_SSL_WARNING="y" \
    guac-metrics-exporter
```

<br>

## Metrics

---

In _Prometheus_ the metrics are called

- number_of_users

- number_of_connection

- number_of_active_connections
  <br><br>

## Limitations

---

This exporter has only been tested using a MySQL database, it should be possible to modify the class variable `api` to support other databases. <br><br>

## Files

---

`guac-metrics.py` - generates the API token, polls _Guacamole_ for the metrics and exposed them for Prometheus.

`config.py` - reads the environment variables.

`metricslogger.py` - stdout logging.

`requirements.txt` - PIP requirements.

# Cloudflare to Datadog Bridge

[![](https://img.shields.io/travis/mozmar/cloudflare-datadog.svg)](https://travis-ci.org/mozmar/cloudflare-datadog)
[![](https://img.shields.io/docker/stars/mozmeao/cloudflare-datadog.svg)](https://hub.docker.com/r/mozmeao/cloudflare-datadog/)
![](https://img.shields.io/imagelayers/image-size/mozmeao/cloudflare-datadog/latest.svg)
![](https://img.shields.io/imagelayers/layers/mozmeao/cloudflare-datadog/latest.svg)

Bridge between Cloudflare Zone Analytics API and Datadog Metrics.

This is built to run as an always-on daemon, fetching data on configurable
intervals from Cloudflare and posting it to Datadog. Cloudflare won't
necessarily return new data every time and the script will make sure to filter
the ones already sent since its start.

Data are posted to Datadog through its HTTP API which allows combinations of
timestamps and values, in contrary to statsd which does not -by design- allow
sending timestamps.


## Setup
Populate the following variables in the environment or a `.env` file.

 - `ZONE`: Cloudflare Zone ID or alternatively use `DOMAIN`
 - `DOMAIN`: Domain or alternatively use `ZONE`
 - `CF_API_EMAIL`: Cloudflare auth email
 - `CF_API_KEY`: Cloudflare auth key
 - `FETCH_INTERVAL`: Fetch every X minutes. (Default: 1)
 - `SINCE`: Since when to fetch data from. (Default: -360)

   Note:
   * Free plans can only get up to 60 min. (Since: -1440)
   * Pro & Business plans can only up to 15 min. (Since: -360)
   * Enterprise plans can get up to 1 min. (Since: -30)

 - `DATADOG_API_KEY`: Datadog API Key
 - `DATADOG_APP_KEY`: Datadog App Key
 - `STATS_KEY_PREFIX`: Prefix for the metrics sent in Datadog.
 - `TAGS`: List of comma separated Datadog Tags

 - `LOG_LEVEL`: Script log level. (Default: INFO)
 - `DEAD_MANS_SNITCH_URL`: A url to ping after every successful submission to
   Datadog. You can use a service
   like [deadmansnitch](http://deadmanssnitch.com/)
   or [healthchecks](http://healthchecks.io/)

 - `TIMEZONE`: Docker only. Set the timezone of the container. (Default: UTC)

### Getting Zone ID

You can provide `DOMAIN` and let the script figure out the Zone ID for you.
Otherwise you can directly provide `ZONE` in the environment.

To get the Zone IDs for your domains populate `CF_API_EMAIL` and `CF_API_KEY` and
run:

```
make build
make shell
./getZoneIDs.py
```

## Run

### Docker

```shell
docker run --env-file .env mozmeao/cloudflare-datadog
```

### Docker custom build

```shell
make build
make run
```

### Virtualenv

```shell
virtualenv venv
. venv/bin/activate
pip install -r requirements.txt
./cloudflare.py
```

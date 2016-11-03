# Cloudflare to Datadog Bridge #

Bridge between Cloudflare Zone Analytics API and Datadog Metrics.

This is built to run as an always-on daemon, fetching data every minute from
Cloudflare and posting it to Datadog. Cloudflare won't necessarily return new
data every minute and the script will make sure to filter the ones already sent
since its start.

Data are posted to Datadog through its HTTP API which allows combinations of
timestamps and values, in contrary to statsd which does not -by design- allow
sending timestamps.


## Instructions
Populate the following variables in the environment or a .env file.

 * *DATADOG_API_KEY*: Datadog API Key
 * *DATADOG_APP_KEY*: Datadog App Key
 * *STATS_KEY_PREFIX*: Prefix for the metrics sent in Datadog.
 * *AUTH_EMAIL*: Cloudflare auth email
 * *AUTH_KEY*: Cloudflare auth key
 * *ZONE*: Cloudflare Zone
 * *TAGS*: List of Datadog Tags


### Shell

Install:

```shell
virtualenv venv
. venv/bin/activate
pip install -r .
```

Run:

```shell
./cloudflare.py
```

### Docker

docker run --env-file .env mozorg/cloudflare-datadog-sync

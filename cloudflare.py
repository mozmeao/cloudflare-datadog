#!/usr/bin/env python

import datetime
import logging

import requests
from apscheduler.schedulers.blocking import BlockingScheduler
from datadog import statsd
from decouple import config


ZONE = config('ZONE')
AUTH_EMAIL = config('AUTH_EMAIL')
AUTH_KEY = config('AUTH_KEY')
URL = ('https://api.cloudflare.com/client/v4/zones/'
       '{}/analytics/dashboard?since=-30'.format(ZONE))
DEAD_MANS_SNITCH_URL = config('DEAD_MANS_SNITCH_URL', None)

scheduler = BlockingScheduler()
until = None

logging.basicConfig(level=logging.INFO)


def ping_dms(function):
    """Pings Dead Man's Snitch after job completion if URL is set."""
    def _ping():
        function()
        if DEAD_MANS_SNITCH_URL:
            utcnow = datetime.datetime.utcnow()
            payload = {'m': 'Run {} on {}'.format(function.__name__, utcnow.isoformat())}
            requests.get(DEAD_MANS_SNITCH_URL, params=payload)
    _ping.__name__ = function.__name__
    return _ping


@scheduler.scheduled_job('interval', minutes=1, max_instances=1, coalesce=True)
@ping_dms
def job_cloudflare2datadog():
    global until
    response = requests.get(URL, headers={
        'X-Auth-Email': AUTH_EMAIL,
        'X-Auth-Key': AUTH_KEY,
        'Content-Type': 'application/json',
    })

    data = response.json()

    timeserries = data['result']['timeseries']
    for timespan in timeserries:
        if until and until != timespan['since']:
            continue
        until = timespan['until']

        for status, value in timespan['requests']['http_status'].items():
            name = 'cloudflare.mozilla-org.g.status_codes.{}'.format(status)
            statsd.gauge(name, value)


def run():

    try:
        scheduler.start()
    except (KeyboardInterrupt, SystemExit):
        pass


if __name__ == '__main__':
    run()

#!/usr/bin/env python
import datetime
import logging
import sys
import time
from collections import defaultdict

import babis
import datadog
import requests
from apscheduler.schedulers.blocking import BlockingScheduler
from decouple import Csv, config
from dateutil import tz


LOG_LEVEL = config('LOG_LEVEL', default='INFO', cast=lambda x: getattr(logging, x))
ZONE = config('ZONE')
AUTH_EMAIL = config('AUTH_EMAIL')
AUTH_KEY = config('AUTH_KEY')
TAGS = config('TAGS', default='source:cloudflare', cast=Csv())
URL = ('https://api.cloudflare.com/client/v4/zones/'
       '{}/analytics/dashboard?since=-30'.format(ZONE))
DEAD_MANS_SNITCH_URL = config('DEAD_MANS_SNITCH_URL', None)
STATS_KEY_PREFIX = config('STATS_KEY_PREFIX', default='cloudflare')
if not STATS_KEY_PREFIX.endswith('.'):
    STATS_KEY_PREFIX += '.'

CLOUDFLARE_HTTP_STATUS_CODES = [200, 206, 301, 302, 304, 400, 403,
                                404, 405, 408, 409, 410, 412, 444,
                                499, 500, 502, 503, 504, 522, 523,
                                524, 525]

logger = logging.getLogger(sys.argv[0])
logging.basicConfig(level=LOG_LEVEL)

scheduler = BlockingScheduler()
until = None
utc_tz = tz.gettz('UTC')
local_tz = tz.gettz()

datadog.initialize(api_key=config('DATADOG_API_KEY'),
                   app_key=config('DATADOG_APP_KEY'))


@scheduler.scheduled_job('interval', minutes=1, max_instances=1, coalesce=True)
@babis.decorator(ping_after=DEAD_MANS_SNITCH_URL)
def job_cloudflare2datadog():
    global until
    logger.debug('Requesting CloudFlare logs')
    response = requests.get(URL, timeout=10, headers={
        'X-Auth-Email': AUTH_EMAIL,
        'X-Auth-Key': AUTH_KEY,
        'Content-Type': 'application/json',
    })
    response.raise_for_status()

    data = response.json()
    timeserries = data['result']['timeseries']
    metrics = defaultdict(list)

    for timespan in timeserries:
        if until and until != timespan['since']:
            continue
        until = timespan['until']

        point = datetime.datetime.strptime(timespan['until'], '%Y-%m-%dT%H:%M:%SZ')
        point = point.replace(tzinfo=utc_tz).astimezone(local_tz)
        timepoint = time.mktime(point.timetuple())

        def _add_data(name, value):
            metrics[name].append((timepoint, value))

        # Status codes
        for status_code in CLOUDFLARE_HTTP_STATUS_CODES:
            value = timespan['requests']['http_status'].get(str(status_code), 0)
            name = STATS_KEY_PREFIX + 'status_codes.{}'.format(status_code)
            _add_data(name, value)

        # Requests
        name = STATS_KEY_PREFIX + 'requests.'
        _add_data(name + 'all', timespan['requests']['all'])
        _add_data(name + 'cached', timespan['requests']['cached'])
        _add_data(name + 'uncached', timespan['requests']['uncached'])
        _add_data(name + 'ssl.encrypted', timespan['requests']['ssl']['encrypted'])
        _add_data(name + 'ssl.unencrypted', timespan['requests']['ssl']['unencrypted'])

        # Bandwidth
        name = STATS_KEY_PREFIX + 'bandwidth.'
        _add_data(name + 'all', timespan['bandwidth']['all'])
        _add_data(name + 'cached', timespan['bandwidth']['cached'])
        _add_data(name + 'uncached', timespan['bandwidth']['uncached'])
        _add_data(name + 'ssl.encrypted', timespan['bandwidth']['ssl']['encrypted'])
        _add_data(name + 'ssl.unencrypted', timespan['bandwidth']['ssl']['unencrypted'])

        # Threats
        name = STATS_KEY_PREFIX + 'threats.'
        _add_data(name + 'all', timespan['threats']['all'])

        # Pageviews
        name = STATS_KEY_PREFIX + 'pageviews.'
        _add_data(name + 'all', timespan['pageviews']['all'])
        for engine, value in timespan['pageviews'].get('search_engines', {}).items():
            _add_data(name + 'search_engines.' + engine, value)

        # IPs
        name = STATS_KEY_PREFIX + 'uniques.'
        _add_data(name + 'all', timespan['uniques']['all'])

    if metrics:
        logger.debug('Sending metrics to Datadog')
        data = [dict(metric=metric, points=points, tags=TAGS) for metric, points in metrics.items()]
        datadog.api.Metric.send(data)
    else:
        logger.debug('No metrics to send to Datadog')



def run():
    try:
        scheduler.start()
    except (KeyboardInterrupt, SystemExit):
        pass


if __name__ == '__main__':
    run()

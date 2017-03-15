import logging

from CloudFlare import CloudFlare
from decouple import Csv, config

LOG_LEVEL = config('LOG_LEVEL', default='INFO', cast=lambda x: getattr(logging, x))
FETCH_INTERVAL = config('FETCH_INTERVAL', default=1, cast=int)
DEAD_MANS_SNITCH_URL = config('DEAD_MANS_SNITCH_URL', None)

# Cloudflare configuration
CF_API_EMAIL = config('CF_API_EMAIL')
CF_API_KEY = config('CF_API_KEY')
ZONE = config('ZONE', default=None)
DOMAIN = config('DOMAIN', default=None)
SINCE = config('SINCE', default='-360')

if (not (ZONE or DOMAIN)) or (ZONE and DOMAIN):
    print('One of ZONE or DOMAIN must be provided')

if DOMAIN:
    cf = CloudFlare(email=CF_API_EMAIL, token=CF_API_KEY)
    ZONE = cf.zones.get(params={'name': DOMAIN})[0]['id']

# Datadog configuration
DATADOG_API_KEY = config('DATADOG_API_KEY')
DATADOG_APP_KEY = config('DATADOG_APP_KEY')
STATS_KEY_PREFIX = config('STATS_KEY_PREFIX', default='cloudflare')
if not STATS_KEY_PREFIX.endswith('.'):
    STATS_KEY_PREFIX += '.'
TAGS = config('TAGS', default='source:cloudflare', cast=Csv())

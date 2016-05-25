import requests
from datadog import statsd
from decouple import config

ZONE = config('ZONE')
AUTH_EMAIL = config('AUTH_EMAIL')
AUTH_KEY = config('AUTH_KEY')

URL = 'https://api.cloudflare.com/client/v4/zones/{}/analytics/dashboard?since=-30'.format(ZONE)

session = requests.Session()
response = session.get(URL, headers={
    'X-Auth-Email': AUTH_EMAIL,
    'X-Auth-Key': AUTH_KEY,
    'Content-Type': 'application/json',
})

data = response.json()
for status, value in data['result']['timeseries'][0]['requests']['http_status'].items():
    name = 'cloudflare.mozilla-org.g.status_codes.{}'.format(status)
    statsd.gauge(name, value)

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
Populate the following variables in the environment or a `.env` file.


  `DATADOG_API_KEY`: Datadog API Key

  `DATADOG_APP_KEY`: Datadog App Key

  `STATS_KEY_PREFIX`: Prefix for the metrics sent in Datadog.

  `AUTH_EMAIL`: Cloudflare auth email

  `AUTH_KEY`: Cloudflare auth key

  `SINCE`: Cloudflare Analytics (based on Plan)

  * Free plan can only get 1 hour period analytics (Since: -1440)
  * Pro & Business plans can only get 15 min. periods (Since: -360)
  * Enterprise can get up to 1 min. period analytics (Since: -30)

  `ZONE`: Cloudflare Zone

How to get Cloudflare zone id:

Populate `AUTH_EMAIL` and `AUTH_KEY` parameters, then:
```
make build
make shell
apk add --no-cache jq curl
curl https://api.cloudflare.com/client/v4/zones?name=example.com \
 -H "X-Auth-Email: $AUTH_EMAIL" -H "X-Auth-Key: $AUTH_KEY" \
 | jq -r .result[].id
```



### Shell

Using Docker:

```
make build
make shell
./cloudflare.py
```

Using virtualenv:

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

```
make build
make run
```

### Deploy to Kubernetes

Push to Registry (update Makefile with registry server applicable)
```
make push
```

Convert environment file to kubernetes secret and create:
```
./env2secret.py -s dd-cf-agent-secret
kubectl apply -f secret.yaml
```

Ensure Registry pull secret exists:
```
kubectl create secret docker-registry honestbee-registry --docker-server=$DOCKER_REGISTRY --docker-username=$DOCKER_USER --docker-password=$DOCKER_PASSWORD --docker-email=$DOCKER_EMAIL
```

Deploy the Pods
```
kubectl apply -f k8s-bundle.yaml
```

### Troubleshooting:

Verify the data encoded in the kubernetes secret:
```
kubectl get secret dd-cf-agent-secret -o json | jq -r .data[] | while read i; do echo
 $i | base64 -D && echo; done
```

When the Kubernetes deployment succeeded, verify the environment variables exist in the pods:
```
kubectl exec -it `kubectl get po -l name=dd-cf-agent -o json | jq -r .items[0].metadata.name` /bin/sh
```

Verify the jobs execute on schedule:
```
kubectl logs -f `kubectl get po -l name=dd-cf-agent -o json | jq -r .items[0].metadata.name`
```

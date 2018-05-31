export CFDD_REPLICAS ?= 1
export CFDD_IMAGE ?= mozmeao/cloudflare-datadog
export CFDD_TAG ?= de54a6462e63c8a288f0e2d33499a5058b712497
export CFDD_IMAGE_PULL_POLICY ?= IfNotPresent
export CFDD_SECRETS_NAME ?= cfdd-secrets
export CFDD_STATS_PREFIX ?= "cfdd"
export CFDD_SINCE ?= "-360"
export CFDD_TAGS ?= ""
export K8S_NAMESPACE ?= cfdd

install:
	j2 cfdd-deployment.yaml.j2 | kubectl apply -n ${K8S_NAMESPACE} -f -


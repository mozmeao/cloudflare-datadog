export CFDD_REPLICAS ?= 1
export CFDD_IMAGE ?= mozmeao/cloudflare-datadog
export CFDD_TAG ?= 32dd3d6539131dff444239d235ad2e79fb498bc9
export CFDD_IMAGE_PULL_POLICY ?= IfNotPresent
export CFDD_SECRETS_NAME ?= cfdd-secrets
export CFDD_STATS_PREFIX ?= "cfdd"
export CFDD_SINCE ?= "-360"
export CFDD_TAGS ?= ""
export K8S_NAMESPACE ?= cfdd

install:
	j2 cfdd-deployment.yaml.j2 | kubectl apply -n ${K8S_NAMESPACE} -f -


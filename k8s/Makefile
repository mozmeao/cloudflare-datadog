export CFDD_REPLICAS ?= 1
export CFDD_IMAGE ?= 1
export CFDD_TAG ?= 1
export CFDD_IMAGE_PULL_POLICY ?= IfNotPresent
export CFDD_SECRETS_NAME ?= cfdd-secrets
export CFDD_STATS_PREFIX ?= "cloudflare-k8s-"
export CFDD_SINCE ?= "-360"
export CFDD_TAGS ?= ""

install:
	j2 cfdd-deployment.yaml.j2 
	#| kubectl apply -n ${K8S_NAMESPACE} -f -
	

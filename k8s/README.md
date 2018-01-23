# Cloudflare -> Datadog in K8s

### Installation

1. Using cfdd-secrets.yaml as a template, populate the values (base64 encoded)
2. `kubectl create namespace cfdd`
3. `kubectl create -f mysecrets.yaml`
4. Look at the defaults in the Makefile, and tweak accordingly. Run `make`.
5. Wait for a few minutes to see stats show up in Datadog



#!/usr/bin/env python
import os,yaml,argparse
from base64 import b64encode

parser = argparse.ArgumentParser(description="convert .env to k8s secret")
parser.add_argument("-i","--input-file", default=".env",
        help=".env file to parse (default=./.env)")
parser.add_argument("-o","--output-file",default="secret.yaml",
        help="yaml file to generate (default=./secret.yaml)")
parser.add_argument("-s","--secret-name",default="mysecret",
        help="name for secret (default=mysecret)")
args = parser.parse_args()

secret = {
    "apiVersion": "v1",
    "kind": "Secret",
    "metadata": {
        "name": args.secret_name
        },
    "type": "Opaque",
    "data": {}
    }
# add secrets from envfile
if not os.path.exists(args.input_file):
    print("{filename} not found".format(filename=args.input_file))
else:
    with open(args.input_file) as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith('#') or '=' not in line:
                continue
            k,v = line.split('=',1)
            v = v.strip()
            k = k.lower().replace('_','-')
            k = ''.join(e for e in k if (e.isalnum() or e == '-'))
            secret['data'][k]=b64encode(v)
# dump secret to yaml
with open(args.output_file,'w') as out:
    yaml.dump(secret,out,default_flow_style=False)

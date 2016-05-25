#!/bin/bash
set -xe

virtualenv venv
. venv/bin/activate
pip install -U -r requirements.txt
python cloudflare.py

#!/bin/sh

set -e

if [ -n "${TIMEZONE}" ]; then
  ln -sf /usr/share/zoneinfo/${TIMEZONE} /etc/localtime
fi

exec "$@"

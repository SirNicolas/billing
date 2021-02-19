#! /usr/bin/env bash
set -e

python /app/app/backend_pre_start.py

bash ./scripts/test.sh "$@"

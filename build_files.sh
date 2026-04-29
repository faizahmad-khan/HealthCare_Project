#!/bin/bash
set -o errexit

python3 -m pip install -r requirements.txt
python3 manage.py collectstatic --noinput

if [ "$RUN_MIGRATIONS" = "1" ]; then
  python3 manage.py migrate --noinput
fi

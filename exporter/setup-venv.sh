#!/bin/sh
set -o errexit
python -m virtualenv .venv
.venv/bin/pip install -r requirements.txt

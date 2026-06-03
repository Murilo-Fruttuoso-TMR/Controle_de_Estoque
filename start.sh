#!/usr/bin/env bash
set -e

if [ -d ".venv" ]; then
  source .venv/bin/activate
fi

waitress-serve --listen=0.0.0.0:5000 run:app

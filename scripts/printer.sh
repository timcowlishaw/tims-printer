#!/bin/bash
. venv/bin/activate
. ./env
python3 scripts/printer.py >/dev/null 2>&1

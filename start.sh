#!/usr/bin/env bash

export FLASK_APP=webpcr.py&&export FLASK_ENV=development&&flask run

echo "press any key to close"
read -n1 slask
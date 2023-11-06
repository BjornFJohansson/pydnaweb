#!/usr/bin/env bash

# eval "$(/home/bjorn/mambaforge/condabin/mamba shell.bash hook)"

mamba activate bjorn311

export FLASK_APP=pydnaweb.py&&export FLASK_ENV=development&&flask run --debug

echo "press any key to close"
read -n1 slask
#!/usr/bin/env bash

eval "$(/home/bjorn/anaconda3/condabin/conda shell.bash hook)"

conda activate flaskapp

export FLASK_APP=pydnaweb.py&&export FLASK_ENV=development&&flask run

echo "press any key to close"
read -n1 slask
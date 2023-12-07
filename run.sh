#!/usr/bin/env bash

# eval "$(/home/bjorn/mambaforge/condabin/mamba shell hook)"

eval "$(/home/bjorn/mambaforge/bin/conda shell.bash hook)"
conda activate bjorn311

# source ~/.lib/mamba/bin/activate

export FLASK_APP=pydnaweb.py&&export FLASK_ENV=development&&flask run --debug

echo "press any key to close"
read -n1 slask

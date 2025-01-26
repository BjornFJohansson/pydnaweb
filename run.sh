#!/usr/bin/env bash

#export PATH="$HOME/bin:$PATH"
#export MAMBA_ROOT_PREFIX="/home/bjorn/miniforge3"
#eval "$(micromamba shell hook --shell bash)"
#micromamba activate bjorn311

# pyenv which python

#export FLASK_APP=pydnaweb.py&&export FLASK_ENV=development&&

flask run --debug

echo "press any key to close"
read -n1 slask

#!/bin/bash

# Optional: activate pyenv environment (if needed)
export PYENV_ROOT="$HOME/.pyenv"
export PATH="$PYENV_ROOT/bin:$PATH"
eval "$(pyenv init --path)"
eval "$(pyenv virtualenv-init -)"

# Run the app using poetry
exec ~/.local/bin/poetry run streamlit run pydnaweb.py

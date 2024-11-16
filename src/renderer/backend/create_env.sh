#!/bin/bash
rm -rf wave_link     

PYTHON_BIN=python3.9
brew update
brew install python@3.9
"$PYTHON_BIN" -m venv wave_link
source wave_link/bin/activate
"$PYTHON_BIN" -m pip install --upgrade pip
"$PYTHON_BIN" -m pip install -r requirements.txt


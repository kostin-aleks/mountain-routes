#!/bin/bash

rm -rf venv
python3 -m venv venv

source venv/bin/activate || exit 0

pip install -r requirements.txt || exit 0



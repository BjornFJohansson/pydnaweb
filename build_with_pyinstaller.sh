#!/usr/bin/env bash

pyinstaller --windowed --onefile --add-data "templates:templates" --add-data "static:static" app.py

echo "press any key to close"
read -n1 slask

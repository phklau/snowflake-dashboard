#!/usr/bin/env bash

source /usr/local/venvs/dashboard/bin/activate
SNOWFLAKE_PATH/proxy/proxy |& PWD/Logger/logToDb.py

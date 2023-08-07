#!/usr/bin/env bash

SNOWFLAKE_PATH/proxy/proxy |& PWD/Logger/logToDb.py

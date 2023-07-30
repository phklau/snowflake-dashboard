#!/usr/bin/env bash

SNOWFLAKE_PATH/snowflake/proxy/proxy |& PWD/Logger/logToDb.py

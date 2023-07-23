#!/usr/bin/env bash


# check for root priviledges

# adapt .service file
# sed
# escape / in pwd!
sed 's/PWD/$PWD/g' ./Settings/logger.json
# move .service file
# only when not existing

# systemctl daemon-reload
# systemctl enable snowflakelogger.service
# systemctl  start snowflakelogger.service

# install python env

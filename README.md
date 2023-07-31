# Snowflake dashboard

To have a more rewarding experience of hosting a snowflake server, snowflake-dashboard is giving an overview of how many people used your snowflake server to avoid censorship.

## Roadmap

- [x] Local beta instance
  - [x] Log output of snowflake into database
  - [x] Build flask app to show data
  - [x] Use nginx/apache to provide flask app
- [ ] automate installation (script/ansible?)
- [ ] Dockerize everything

# Installation

Main branch provides currently all nessesary scripts and can be used in production. 
Automated installation is under development.

## Logger

- install snowflake proxy
  (https://community.torproject.org/relay/setup/snowflake/standalone/)
- adapt path to snowflake proxy in 'run.sh'
- adapt INSTALL_PATH, USER and GROUP in `snowflakelogger.service`
- adapt `Settings/logger.json`
- setup systemd service to run snowflake proxy with logging into the database:
```
cp snowflakelogger.service /etc/systemd/system/
systemctl daemon-reload
systemctl enable snowflakelogger.service
systemctl start snowflakelogger.service
systemctl status snowflakelogger.service
```

## Dashboard

- install pip requirments (use virtual environment to dont mess up your system
  python!), `requirments.txt` could be found in `feat/installation`-branch
- setup wsgi server, calling wsgi-application in `app_wsgi.py` 

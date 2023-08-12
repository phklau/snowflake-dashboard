# Snowflake dashboard

To have a more rewarding experience of hosting a snowflake server, snowflake-dashboard is giving an overview of how many people used your snowflake proxy to avoid censorship.

This project provides:
- python script to log the output of the snowflake proxy in a database
- systemd service to run the proxy with logging in the backround
- wsgi-application that displays the logs from the database in a web dashboard
- apache configuration to run the wsgi-application

The logger and wsgi-application can also be used with another init-system and
another webserver.

## Roadmap

- [x] Local beta instance
  - [x] Log output of snowflake into database
  - [x] Build flask app to show data
  - [x] Use nginx/apache to provide flask app
- [x] automate installation 
- [ ] Dockerize everything

# Installation

## Automated

Requirments:
- snowflake proxy
  (https://community.torproject.org/relay/setup/snowflake/standalone/)
- systemd
- python3
- bash

Run `./install.sh -i` to install the logger and the dashboard (needs root
priviledges).
See `./install.sh -h` for more options.
After the first run the script initalizes a file in `Installation/InstallationSettings.bash`
for settings that are needed during the installation.
Fill out the required fields and then rerun the script.

To update the app after installation pull the current version from git and then
run `./install.sh -u`.
This restarts the systemd service of the logger to use the update logger and
copys the new dashboard to the webserver.
To only update the web app run `./install.sh --update-dashboard`.

**Warning:** Make a backup befor running this script!
The script has only yet been tested on a fresh installation of debian-bookworm.

## Manual

You can also install the logger and wsgi-application by hand.
All preconfigured files for apache and systemd can be found in
`Installation/templates`.

The logger and wsgi-application rely on JSON settings files.
Those have to be located in the root of the repo in a directory called
`Settings`. When installing manual, copy the template files and adapt the
settings according to your installation.
```
mkdir Settings
cp Installation/templates/*json Settings
```

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

The logger is a python script that reads in the output of the proxy and stores it to
the database. You need to redirect stdout and stderr to the logger script.
This is done in the run.sh script. When using a different shell and/or a
different init-system you have to set this up by your self.

## Dashboard

- install pip requirments (use virtual environment to dont mess up your system
  python!), `requirments.txt` could be found in `Dashboard/` 
- setup wsgi server, calling wsgi-application in `app_wsgi.py` 

#!/usr/bin/env bash

# set -x
set -e


usage () {
    cat <<EOF
Usage: 
-h| --help
-i| --install           Install new application
    --install-service   Install only the systemd service running snowflake with logging
-u| --update-all        Update your installed application
    --update-dasboard   Update only the dashboard
-d| --deinstall         Delete all generated system files (without logs)
EOF
exit
}


preinstall_check () {
            echo "Installing ..."
            if [ -d "./Settings/" ]; then
                echo "It seems like you have already installed this app"
                echo "use -u to update the app"
                echo "Aborting ..."
                exit
            fi
            if [ "$(id -u)" -ne 0 ]; then
                echo "Run skript as root"
                echo "Aborting ..."
                exit
            fi
            if [ ! -f "Installation/InstallationSettings.bash" ]; then
                cp ./Installation/templates/InstallationSettings.bash ./Installation/
                echo "Created installation settings file"
                echo "please set the variables and rerun this script"
                exit
            fi
            load_settings
}

load_settings () {
            source ./Installation/InstallationSettings.bash
            WEBAPP_PATH=${WEBAPP_PATH%/}
            SNOWFLAKE_PATH=${SNOWFLAKE_PATH%/}

            if [[ $SNOWFLAKE_PATH == "" || $SNOWFLAKE_USER == "" || $SNOWFLAKE_GROUP == "" || SERVER_NAME == "" ]]; then
                echo "No snowflake settings found"
                echo "Please check again InstallationSettings.bash"
                echo "Aborting ..."
                exit
            fi
}

create_settings () {
    echo "Creating setting files in $PWD/Settings"
    mkdir ./Settings/
    cp ./Installation/templates/*.json ./Settings/
    chown -R ${SNOWFLAKE_USER}:${SNOWFLAKE_GROUP} ./Settings/
    sed -i "s/PWD/${PWD//\//\\/}/g" ./Settings/dashboard.json
}

create_data_storage () {
    echo "Creating log storage in /var/log/snowflake/"
    if [ ! -d /var/log/snowflake/ ]; then
        mkdir /var/log/snowflake/
    fi
    chown $SNOWFLAKE_USER:$SNOWFLAKE_GROUP /var/log/snowflake/
}

install_packages () {
    apt install python3-venv apache2 libapache2-mod-wsgi-py3
    systemctl restart apache2
}

create_pyenv () {
    echo "Creating python evironment in /usr/local/venvs/dashboard"
    LAST_PATH=$PWD
    if [ ! -d /usr/local/venvs ]; then
        mkdir -p /usr/local/venvs
    fi
    cd /usr/local/venvs
    python3 -m venv dashboard
    source dashboard/bin/activate
    pip install -r ${LAST_PATH}/Dashboard/requirements.txt
    deactivate
    cd ${LAST_PATH}
}

create_systemd_service () {
    echo "Creating systemd service snowflake-with-logger.service"
    cp ./Installation/templates/snowflake-with-logger.service /etc/systemd/system/ 
    cp ./Installation/templates/run.sh .
    chown ${SNOWFLAKE_USER}:${SNOWFLAKE_GROUP} run.sh
    sed -i "s/INSTALLATION_PATH/${PWD//\//\\/}/g" /etc/systemd/system/snowflake-with-logger.service
    sed -i "s/USER/${SNOWFLAKE_USER}/g" /etc/systemd/system/snowflake-with-logger.service
    sed -i "s/GROUP/${SNOWFLAKE_GROUP}/g" /etc/systemd/system/snowflake-with-logger.service
    sed -i "s/PWD/${PWD//\//\\/}/g" ./run.sh
    sed -i "s/SNOWFLAKE_PATH/${SNOWFLAKE_PATH//\//\\/}/g" ./run.sh
    systemctl daemon-reload
    systemctl enable snowflake-with-logger.service
    systemctl start snowflake-with-logger.service
    sleep 5
    systemctl status snowflake-with-logger.service
}

install_apache () {
    echo "Installing dashboard web app..."
    systemctl stop apache2
    mkdir -p $WEBAPP_PATH
    cp -R ${PWD}/Dashboard $WEBAPP_PATH
    cp -R ${PWD}/Settings $WEBAPP_PATH
    chown -R www-data:www-data $WEBAPP_PATH/
    systemctl start apache2
    echo "Activating config /etc/apache2/sites-available/snowflake-dashboard.conf"
    cp ./Installation/templates/snowflake-dashboard.conf /etc/apache2/sites-available/
    sed -i "s/WEBAPP_PATH/${WEBAPP_PATH//\//\\/}/g" /etc/apache2/sites-available/snowflake-dashboard.conf
    sed -i "s/SERVER_NAME/${SERVER_NAME}/g" /etc/apache2/sites-available/snowflake-dashboard.conf
    a2ensite snowflake-dashboard
    echo "Restart apache"
    systemctl restart apache2
}

update_web_app () {
            echo "Updating webapp ..."
            systemctl stop apache2
            rm -rf $WEBAPP_PATH
            mkdir -p $WEBAPP_PATH
            cp -R ${PWD}/Dashboard $WEBAPP_PATH
            cp -R ${PWD}/Settings $WEBAPP_PATH
            chown -R www-data:www-data $WEBAPP_PATH/
            systemctl start apache2
}

deinstall () {
    echo "Remove Settings"
    rm -rf ./Settings
    echo "Remove snowflake-dashboard.conf"
    rm /etc/apache2/sites-enabled/snowflake-dashboard.conf
    rm /etc/apache2/sites-available/snowflake-dashboard.conf
    echo "Remove $WEBAPP_PATH"
    rm -rf $WEBAPP_PATH
    echo "Remove run.sh"
    rm run.sh
    echo "Remove systemd service"
    systemctl stop snowflake-with-logger.service
    systemctl disable snowflake-with-logger.service
    rm /etc/systemd/system/snowflake-with-logger.service
    systemctl daemon-reload
    echo "Remove python environment"
    rm -rf /usr/local/venvs/dashboard
}

main () {
    if [ "$#" -ne 1 ]; then
        usage
    else
        case $1 in
            -u | --update-all)
                echo "Updating snowflake with logging service ..."
                systemctl restart snowflake-with-logger.service
                load_settings
                update_web_app
                ;;
            --update-dashboard)
                load_settings
                update_web_app
                ;;
            -i | --install)
                preinstall_check
                install_packages
                # Logger
                create_settings
                create_data_storage
                create_systemd_service
                # Dashboard
                create_pyenv
                install_apache
                ;;

            --install-service)
                preinstall_check
                create_settings
                create_data_storage
                create_systemd_service
                ;;

            -d | --deinstall)
                echo "Deinstalling ..."
                deinstall
                ;;
            *)
                usage
                ;;
        esac
    fi
}

main "$@"

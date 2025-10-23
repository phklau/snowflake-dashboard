#!/usr/bin/env bash

# set -x
set -e

SUPPORTED_SNOWFLAKE_VERSION="2.11.0"
VERSION_REGEX='[0-9]+\.[0-9]+\.?[0-9]+'


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
                echo "Created installation settings file Installation/InstallationSettings.bash"
                echo "please set the variables  and rerun this script"
                exit
            fi
            load_settings
}

load_settings () {
            source ./Installation/InstallationSettings.bash
            WEBAPP_PATH=${WEBAPP_PATH%/}
            SNOWFLAKE_PATH=${SNOWFLAKE_PATH%/}

            if [[ $SNOWFLAKE_PATH == "" || $SNOWFLAKE_USER == "" || $SNOWFLAKE_GROUP == "" || $SERVER_NAME == "" ]]; then
                echo "Some of the snowflake settings variables might be empty"
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
    set_snowflake_version
}

# needs load_settings() run
set_snowflake_version () {
    SNOWFLAKE_VERSION=$($SNOWFLAKE_PATH/proxy/proxy --version 2>&1 | grep -o -E $VERSION_REGEX)
    echo "Snowflake version $SNOWFLAKE_VERSION detected"
    if dpkg --compare-versions $SNOWFLAKE_VERSION gt $SUPPORTED_SNOWFLAKE_VERSION; then
        echo "WARNING!: snowflake version is not supported and might cause problems parsing the logs"
        echo "Check the database if logs for errors of the type <Parser>"
    fi
    sed -i s/"[0-9]\+\.[0-9]\+\.[0-9]\+"/${SNOWFLAKE_VERSION}/g ./Settings/logger.json
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

check_python_version () {
    SUPPORTED_VERSIONS=("3.11.2" "3.13.5")
    VERSION=$(python3 --version | grep -o -E $VERSION_REGEX)
    SUPPORTED=false

    for value in "${SUPPORTED_VERSIONS[@]}"
    do
        if [ "$value" = "$VERSION" ]; then
            SUPPORTED=true
            break
        fi
    done

    if $SUPPORTED; then
        echo $VERSION | sed -E 's/\./-/g'
    fi
}

create_pyenv () {
    echo "Checking if installed python version is supported ..."
    VERSION=$(check_python_version)
    if [ -z $VERSION ]; then
        echo "Python Version not supported, please check the manual"
        exit
    fi
    echo "Creating python evironment in /usr/local/venvs/dashboard"
    LAST_PATH=$PWD
    if [ ! -d /usr/local/venvs ]; then
        mkdir -p /usr/local/venvs
    fi
    cd /usr/local/venvs
    python3 -m venv dashboard
    source dashboard/bin/activate
    pip install -r ${LAST_PATH}/Dashboard/requirements_${VERSION}.txt
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
    a2ensite snowflake-dashboard.conf
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
                load_settings
                set_snowflake_version
                systemctl restart snowflake-with-logger.service
                update_web_app
                ;;
            --update-dashboard)
                load_settings
                update_web_app
                ;;
            -i | --install)
                preinstall_check
                install_packages
                create_settings
                # Dashboard
                create_pyenv
                install_apache
                # Logger
                create_data_storage
                create_systemd_service
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

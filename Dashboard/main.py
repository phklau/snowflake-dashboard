from dash import Dash
import json

with open("../Settings/settings.json") as settings_file
    settings = json.load(settings_file)
DB_PATH = settings["Path to database"]

if __name__ == '__main__':
    try:
        logs = SnowflakeLogs(PATH_TO_DB)
    except Warning:
        print("No connection established")
    else:
        # print(logs.figure_data_connections_at_day(datetime.today() - timedelta(days=20)))
        print(logs.getDirectDbAccess().running_since())
        connections = logs.get_connections_between(datetime(2022, 12, 30, 17, 00, 30),datetime(2022, 12, 30, 20, 00, 50))
        print(connections)
        print(connections["Connections"])

# read DB path from config file?
# make table variable?
# connect db
# build app


#     app.run_server(debug=True)

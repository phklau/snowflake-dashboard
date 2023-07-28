from dash import Dash
import json

import layout
import callbacks

with open("../Settings/testsettings.json") as settings_file:
    settings = json.load(settings_file)
DB_PATH = settings["Path to database"]

app = Dash(__name__)
app = layout.build_layout(app)
app = callbacks.get_callbacks(app)

if __name__ == '__main__':
    app.run_server(debug=True)
#    try:
#        logs = SnowflakeLogs(DB_PATH)
#    except Warning:
#       print("No connection established")
#    else:
#        # print(logs.figure_data_connections_at_day(datetime.today() - timedelta(days=20)))
#        print(logs.getDirectDbAccess().running_since())
#        connections = logs.get_connections_between(datetime(2022, 12, 30, 17, 00, 30),datetime(2022, 12, 30, 20, 00, 50))
#        print(connections)
#        print(connections["Connections"])

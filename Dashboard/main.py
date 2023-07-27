from dash import Dash
import json

import layout

with open("../Settings/testsettings.json") as settings_file:
    settings = json.load(settings_file)
DB_PATH = settings["Path to database"]

app = Dash(__name__)
app = layout.build_layout(app)

if __name__ == '__main__':
    app.run_server(debug=True)

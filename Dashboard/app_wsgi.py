#!PWD/Dashboard/dashenv/bin/python3

import sys
import json
from dash import Dash

from App import layout, callbacks

app = Dash(__name__)
app = layout.build_layout(app)
app = callbacks.get_callbacks(app)
app.css.config.serve_locally = True

with open("../Settings/dashboard.json") as settings_file:
    settings = json.load(settings_file)
APP_PATH = settings["Path to app"]
if APP_PATH not in sys.path:
    sys.path = [APP_PATH] + sys.path

application = app.server

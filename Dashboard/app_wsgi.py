import sys
from pathlib import Path

from dash import Dash

APP_PATH = str(Path(__file__).parent)
if APP_PATH not in sys.path:
    sys.path.append(APP_PATH)

from App import layout, callbacks

app = Dash(__name__)
app = layout.build_layout(app)
app = callbacks.get_callbacks(app)
app.css.config.serve_locally = True
app.scripts.config.serve_locally = True


application = app.server

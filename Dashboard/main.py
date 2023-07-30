from dash import Dash

import layout
import callbacks

app = Dash(__name__)
app = layout.build_layout(app)
app = callbacks.get_callbacks(app)
app.css.config.serve_locally = True

if __name__ == '__main__':
    app.run_server(debug=True)

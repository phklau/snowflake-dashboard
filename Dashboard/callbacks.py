from dash import Dash, callback, Input, Output, ctx
from datetime import datetime, date, timedelta
import json

from SnowflakeLogs import SnowflakeLogs
from format import DataSize

with open("../Settings/testsettings.json") as settings_file:
    settings = json.load(settings_file)
DB_PATH = settings["Path to database"]


def get_callbacks(app: Dash):

    @app.callback(
        Output('date-picker', 'start_date'),
        Output('date-picker', 'end_date'),
        Input('day-button', 'n_clicks'),
        Input('week-button', 'n_clicks'),
        Input('month-button', 'n_clicks'),
    )
    def update_date_picker(day, week, month):
        end_date = date.today()
        time_range = {
            None: timedelta(0),
            "day-button": timedelta(0),
            "week-button": timedelta(days=7),
            "month-button": timedelta(weeks=4),
        }
        pressed_button = ctx.triggered_id
        start_date = end_date - time_range.get(pressed_button)
        return (
            start_date,
            end_date
        )

    @app.callback(
        Output('total-connections', 'children'),
        Output('total-upload', 'children'),
        Output('total-download', 'children'),
        Output('total-errors', 'children'),
        Input('date-picker', 'start_date'),
        Input('date-picker', 'end_date'),
    )
    def update_metrics(start_date_iso, end_date_iso):
        start_date = datetime.fromisoformat(start_date_iso)
        end_date = datetime.fromisoformat(end_date_iso)

        logs = SnowflakeLogs(DB_PATH)
        logs.load_section_in_buffer(start_date, end_date)

        total_connections = "{:,}".format(logs.get_total_connections())
        total_upload = DataSize(logs.get_total_upload()).auto_format()
        total_download = DataSize(logs.get_total_download()).auto_format()
        total_errors = logs.get_total_errors()

        del logs
        return(
            total_connections,
            total_upload,
            total_download,
            total_errors,
        )
    return app

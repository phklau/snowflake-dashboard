from dash import Dash, Input, Output, ctx, html
from datetime import datetime, date, timedelta
import plotly.express as px
import json

from Data.SnowflakeLogs import SnowflakeLogs
from Helpers.format import DataSize
from Helpers.GraphCreator import GraphCreator

with open("../../Settings/testsettings.json") as settings_file:
    settings = json.load(settings_file)
DB_PATH = settings["Path to database"]


def get_callbacks(app: Dash):
    @app.callback(
        Output('date-picker', 'start_date'),
        Output('date-picker', 'end_date'),
        Output('day-button', 'className'),
        Output('week-button', 'className'),
        Output('month-button', 'className'),
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
        buttons_style = {
            None: "",
            "day-button": "button ml-1 is-light is-medium",
            "week-button": "button ml-1 is-light is-medium",
            "month-button": "button ml-1 is-light is-medium",
        }
        buttons_style[pressed_button] = "button ml-1 is-light is-medium is-focused is-active"

        return (
            start_date,
            end_date,
            buttons_style["day-button"],
            buttons_style["week-button"],
            buttons_style["month-button"],
        )

    @app.callback(
        Output('total-connections', 'children'),
        Output('total-upload', 'children'),
        Output('total-download', 'children'),
        Output('total-errors', 'children'),
        Output('connections-graph', 'figure'),
        Output('upload-download-graph', 'figure'),
        Output('error-graph', 'figure'),
        Output('error-types-pie', 'figure'),
        Output('error-types-bar', 'figure'),
        Input('date-picker', 'start_date'),
        Input('date-picker', 'end_date'),
    )
    def update_metrics(start_date_iso, end_date_iso):
        start_date = datetime.fromisoformat(start_date_iso)
        end_date = datetime.fromisoformat(end_date_iso)

        logs = SnowflakeLogs(DB_PATH)
        logs.load_section_in_buffer(start_date, end_date)
        if logs.buffer_empty():
            # TODO: Pop up/better error handling?
            total_connections = "No Data available"
            total_upload = "No Data available"
            total_download = "No Data available"
            total_errors = "No Data available"
            connections_fig = px.line()
            upload_download_fig = px.line()
            error_fig = px.line()
            error_pie = px.pie()
            error_bar = px.bar()
        else:
            total_connections = "{:,}".format(logs.get_total_connections())
            total_upload = DataSize(logs.get_total_upload()).auto_format()
            total_download = DataSize(logs.get_total_download()).auto_format()
            total_errors = logs.get_total_errors()

            creator = GraphCreator(logs.get_buffered_logs())
            connections_fig = creator.create_connections_graph()
            upload_download_fig = creator.create_upload_download_graph()
            error_fig = creator.create_error_graph()
            error_pie = creator.create_error_pie()
            error_bar = creator.create_error_bar()

        del logs
        return (
            [html.Img(className="mr-3", src='../assets/connection.svg', style={'width': '25px', 'height': '25px'}),
             total_connections],
            [html.Img(className="mr-3", src='../assets/arrow-up-bold.svg', style={'width': '25px', 'height': '25px'}),
             total_upload],
            [html.Img(className="mr-3", src='../assets/arrow-down-bold.svg', style={'width': '25px', 'height': '25px'}),
             total_download],
            [html.Img(className="mr-3", src='../assets/alert-circle.svg', style={'width': '25px', 'height': '25px'}),
             total_errors],
            connections_fig,
            upload_download_fig,
            error_fig,
            error_pie,
            error_bar,
        )

    return app

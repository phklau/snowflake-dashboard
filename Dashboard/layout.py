from dash import Dash, html, dcc
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from dash.dcc import DatePickerRange


def build_layout(app: Dash):
    app.layout = html.Div(className="container is-fluid", children=[
        build_header(),
        build_description_text(),
        build_selector(),
        build_characteristic_values(),
        build_charts_(),
    ])
    return app


def build_header():
    title = html.H1(className="title is-1 has-text-centered", children="Snowflake Dashboard")
    div = html.Div(className="block mt-4", children=[title])
    return div


def build_description_text():
    link = html.A(children="https://snowflake.torproject.org", href="https://snowflake.torproject.org")
    text = """
    This network is running a Snowflake-Proxy for
        the TOR-Network to
    help people overcome censorship and surveillance.
    For more info visit: 
    """
    div = html.Div(className="block has-text-centered is-family-monospace", children=[html.P(children=[text, link])])
    return div


def build_selector():
    date_range = dcc.DatePickerRange(id='date-picker')
    day_button = html.Button(className="button ml-5 is-light is-medium",
                             id='day-button', children="24h")
    week_button = html.Button(className="button ml-1 is-light is-medium",
                              id='week-button', children="Week")
    month_button = html.Button(className="button ml-1 is-light is-medium",
                               id='month-button', children="Month")
    div = html.Div(className="block", children=[
        date_range,
        day_button,
        week_button,
        month_button,
    ])
    return div


def build_characteristic_values():
    connections = html.Div(className="column",
                           children=[
                               html.Div(className="box", children=[
                                   html.P(className="title is-3 has-text-centered",
                                          children="13"),
                                   html.H1(className="title is-6 has-text-centered",
                                           children="Connections")
                               ])
                           ])
    upload = html.Div(className="column",
                      children=[
                          html.Div(className="box", children=[
                              html.P(className="title is-3 has-text-centered",
                                     children="500 GB"),
                              html.H1(className="title is-6 has-text-centered",
                                      children="Upload")
                          ])
                      ])
    download = html.Div(className="column",
                        children=[
                            html.Div(className="box", children=[
                                html.P(className="title is-3 has-text-centered",
                                       children="12 GB"),
                                html.H1(className="title is-6 has-text-centered",
                                        children="Download")
                            ])
                        ])
    errors = html.Div(className="column",
                        children=[
                            html.Div(className="box", children=[
                                html.P(className="title is-3 has-text-centered",
                                       children="12"),
                                html.H1(className="title is-6 has-text-centered",
                                        children="Errors")
                            ])
                        ])
    columns = html.Div(className="columns", children=[connections, upload, download, errors])
    div = html.Div(className="block", children=[columns])
    return div


def build_charts_():
    connections = html.Div(className="column",
                           children=[
                               html.Div(className="box",
                                        children=[
                                            dcc.Graph()
                                        ])
                           ])
    upload = html.Div(className="column",
                      children=[
                          html.Div(className="box",
                                   children=[
                                       dcc.Graph()
                                   ]
                                   )])
    download = html.Div(className="column",
                        children=[
                            html.Div(className="box",
                                     children=[
                                         dcc.Graph()
                                     ])
                        ])
    columns = html.Div(className="columns", children=[connections, upload, download])
    div = html.Div(className="block", children=[columns])
    return div

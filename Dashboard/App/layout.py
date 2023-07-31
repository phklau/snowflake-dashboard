from dash import Dash, html, dcc


def build_layout(app: Dash):
    app.layout = html.Div(className="container mt-0 is-fluid",  children=[
        build_header(),
        build_description_text(),
        build_selector(),
        build_characteristic_values(),
        build_charts_(),
    ])
    return app


def build_header():
    title = html.H1(className="title is-1 has-text-centered has-text-grey-lighter",
                    children="Snowflake Dashboard ❄️")
    div = html.Div(className="block mt-4", children=[title])
    return div


def build_description_text():
    link = html.A(className="has-text-link-light",
                  children="https://snowflake.torproject.org",
                  href="https://snowflake.torproject.org")
    text = """
    This network is running a Snowflake-Proxy for
        the TOR-Network to
    help people overcome censorship and surveillance.
    For more info visit: 
    """
    div = html.Div(className="block has-text-centered is-family-monospace has-text-light",
                   children=[html.P(children=[text, link])])
    return div


def build_selector():
    # TODO: Add settings for displayed dateformat
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
                                          id="total-connections",
                                          children="13"),
                                   html.H1(className="subtitle is-6 has-text-centered",
                                           children="Connections")
                               ])
                           ])
    upload = html.Div(className="column",
                      children=[
                          html.Div(className="box", children=[
                              html.P(className="title is-3 has-text-centered",
                                     id="total-upload",
                                     children="500 GB"),
                              html.H1(className="subtitle is-6 has-text-centered",
                                      children="Upload")
                          ])
                      ])
    download = html.Div(className="column",
                        children=[
                            html.Div(className="box", children=[
                                html.P(className="title is-3 has-text-centered",
                                       id="total-download",
                                       children="12 GB"),
                                html.H1(className="subtitle is-6 has-text-centered",
                                        children="Download")
                            ])
                        ])
    errors = html.Div(className="column",
                      children=[
                          html.Div(className="box", children=[
                              html.P(className="title is-3 has-text-centered",
                                     id="total-errors",
                                     children="12"),
                              html.H1(className="subtitle is-6 has-text-centered",
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
                                            html.H1(className="subtitle", children="Connections"),
                                            dcc.Graph(id="connections-graph"),
                                        ])
                           ])

    error = html.Div(className="column",
                     children=[
                         html.Div(className="box",
                                  children=[
                                      html.H1(className="subtitle", children="Errors"),
                                      dcc.Graph("error-graph")
                                  ])
                     ])

    traffic = html.Div(className="column",
                       children=[
                           html.Div(className="box",
                                    children=[
                                        html.H1(className="subtitle", children="Traffic"),
                                        dcc.Graph(id="upload-download-graph")
                                    ]),
                       ])

    errortypes = html.Div(className="column",
                          children=[
                              html.Div(className="box", children=[
                                  html.Div(className="columns", children=[
                                      html.H1(className="subtitle", children="Errortypes"),
                                      html.Div(className="column", children=dcc.Graph("error-types-pie")),
                                      html.Div(className="column", children=dcc.Graph("error-types-bar"))
                                  ]),
                              ]),
                          ])

    connections_error = html.Div(className="block mb-1", children=html.Div(className="columns", children=[connections, error,]))
    traffic_errortypes = html.Div(className="block", children=html.Div(className="columns ", children=[traffic, errortypes, ]))
    div = html.Div(className="block", children=[connections_error, traffic_errortypes])
    return div

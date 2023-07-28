from dash import Dash, callback, Input, Output, ctx
from datetime import datetime, date, timedelta


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
    # TODO: generate data according to picked data range

    return app

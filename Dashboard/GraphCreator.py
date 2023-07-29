import plotly.express as px
from plotly import graph_objects
import pandas as pd
from datetime import datetime, date, timedelta


class GraphCreator:

    def __init__(self, data: pd.DataFrame):
        self.data = data
        time_range = self.data.tail(1)["Timestamp"].item() - self.data.head(1)["Timestamp"].item()
        self.data = data.set_index("Timestamp")
        if time_range > timedelta(weeks=2):
            intervall = timedelta(days=1)
            self.data = self.data.resample(intervall).sum()

    @staticmethod
    def __get_line_graph_prototype():
        graph = px.line()
        graph.update_layout(
            plot_bgcolor='rgb(255,200,255)',
            paper_bgcolor='rgb(255,255,255)',
            xaxis_title=None,
            yaxis_title=None,
            margin={'l': 10, 'r': 10, 't': 10, 'b': 10},
        )
        return graph


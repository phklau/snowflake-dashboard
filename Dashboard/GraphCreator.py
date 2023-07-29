import plotly.express as px
from plotly import graph_objects
import pandas as pd
from datetime import datetime, date, timedelta


class GraphCreator:

    def __init__(self, data: pd.DataFrame):
        data = data.set_index("Timestamp")
        data.sort_index(inplace=True)
        self.traffic_data = data[["Connections", "Upload", "Download"]]
        self.error_data = data[["Error", "Errortype", "Details"]]
        time_range = self.traffic_data.tail(1).index.item() - self.traffic_data.head(1).index.item()
        if time_range > timedelta(weeks=2):
            intervall = timedelta(days=1)
            self.traffic_data = self.traffic_data.resample(intervall).sum()

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

    def create_connections_graph(self):
        connections_data = self.traffic_data
        graph = self.__get_line_graph_prototype()
        max_value = self.traffic_data["Connections"].max()
        graph.update_layout(yaxis_range=[0, max_value * 1.1], height=150)
        trace = graph_objects.Scatter(x=connections_data.index, y=connections_data["Connections"],
                                      line={'color': "dodgerblue"})
        graph.add_trace(trace)
        return graph

    def create_upload_download_graph(self):
        upload_key = "Upload"
        download_key = "Download"
        download_data_inverted = self.traffic_data[download_key].multiply(-1)
        graph = self.__get_line_graph_prototype()
        max_upload = self.traffic_data[upload_key].max()
        max_download = download_data_inverted.min()
        graph.update_layout(yaxis_range=[max_download * 1.1, max_upload * 1.1],
                            height=150,
                            yaxis={'ticksuffix': " MB"},
                            legend={'orientation': "h", 'yanchor': "top", 'y': 0, 'xanchor': "right", 'x': 1})
        upload_trace = graph_objects.Scatter(x=self.traffic_data.index, y=self.traffic_data[upload_key], name="Upload",
                                             fill='tozeroy')
        download_trace = graph_objects.Scatter(x=self.traffic_data.index, y=download_data_inverted, name="Download",
                                               fill='tozeroy')
        graph.add_trace(download_trace)
        graph.add_trace(upload_trace)
        return graph

    def create_error_graph(self):
        graph = self.__get_line_graph_prototype()
        graph.update_layout(yaxis_range=[-0.1, 1.1], height=150)
        error_trace = graph_objects.Scatter(x=self.error_data.index, y=self.error_data["Error"])
        graph.add_trace(error_trace)
        return graph

    def create_error_pie(self):
        data = self.error_data[self.error_data["Error"] == 1]
        graph = px.pie(data, names='Errortype')
        graph.update_traces(textinfo='none')
        graph.update_layout(height=150,
                            margin={'l': 0, 'r': 0, 't': 0, 'b': 0},
                            showlegend=True,
                            legend={'yanchor': "middle", 'y': 0.5, 'xanchor': "right", 'x': 0},
                            )
        return graph

    def create_error_bar(self):
        data = self.error_data[self.error_data["Error"] == 1]
        graph = px.histogram(
            data,
            y='Errortype',
            orientation='h',
            color='Errortype',
            barmode='group'
        )
        graph.update_layout(height=150,
                            margin={'l': 0, 'r': 0, 't': 0, 'b': 0},
                            xaxis_title=None,
                            yaxis_title=None,
                            yaxis_visible=False,
                            plot_bgcolor='rgb(255,255,255)',
                            paper_bgcolor='rgb(255,255,255)',
                            showlegend=False,
                            )
        return graph

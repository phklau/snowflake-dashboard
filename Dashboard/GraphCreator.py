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


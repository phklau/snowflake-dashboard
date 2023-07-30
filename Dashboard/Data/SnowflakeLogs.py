import pandas

from Data.SqliteDB import SqliteDB
from datetime import datetime, timedelta
import pandas as pd


class SnowflakelogDB(SqliteDB):
    """
    interacts with the sqlite db storing the logs
    """

    DATE_TIME_FORMAT = "%Y-%m-%d %H:%M:%S"

    def logging_since(self):
        statement = """
        SELECT Timestamp FROM logdata ORDER BY ID LIMIT 1 
        """
        return self.query_data(statement)

    def running_since(self):
        statement = """
        SELECT Timestamp FROM logdata WHERE Details = 'Proxy starting' ORDER BY ID DESC LIMIT 1 
        """
        return self.query_data(statement)

    def get_logs_between(self, date_from: datetime, date_till: datetime):
        statement = """
        SELECT * 
        FROM logdata 
        WHERE Timestamp BETWEEN ?
        AND ? 
        """
        logs = self.query_data(statement,
                               (date_from.strftime("%Y-%m-%d %H:%M:%S"), date_till.strftime("%Y-%m-%d %H:%M:%S")))
        return logs


# Errors
# Down/Upstreams

# SnowFlakeLogs
class SnowflakeLogs:
    """
    API providing the required data for the dashboard
    """

    def __init__(self, pathtodb: str):
        self.__db = SnowflakelogDB(pathtodb)
        self.__buffer = pd.DataFrame()
        if not self.__db.is_db_connected():
            raise Warning("Couldn't connect to db")

    def __del__(self):
        self.__db.close_connection()

    def __query_data(self, date_from: datetime, date_till: datetime):
        data = self.__db.get_logs_between(date_from, date_till)
        data_dict = {
            "ID": list(map(lambda x: x[0], data)),
            "Timestamp": list(
                map(lambda x: datetime.strptime(x[1], SnowflakelogDB.DATE_TIME_FORMAT), data)),
            "Error": list(map(lambda x: x[2], data)),
            "Errortype": list(map(lambda x: x[3], data)),
            "Details": list(map(lambda x: x[4], data)),
            "Connections": list(map(lambda x: x[5], data)),
            "Upload": list(map(lambda x: x[6], data)),
            "Download": list(map(lambda x: x[7], data)),
        }
        self.__buffer = pd.DataFrame(data_dict)

    # if grouping is needed (show whole week-->sum up to days), to it here
    # or https://plotly.com/python/time-series/ (Displaying Period Data)
    # https://datagy.io/pandas-datetime/

    def __format_sql_to_datetime(self, timestamp: str) -> datetime:
        return datetime.strptime(timestamp, SnowflakelogDB.DATE_TIME_FORMAT)

    def load_section_in_buffer(self, date_from: datetime, date_till: datetime):
        self.__query_data(date_from, date_till)

    def get_total_connections(self):
        return self.__buffer["Connections"].sum()

    def get_total_download(self):
        return self.__buffer["Download"].sum()

    def get_total_upload(self):
        return self.__buffer["Upload"].sum()

    def get_total_errors(self):
        return self.__buffer["Error"].sum()

    def get_connections(self) -> pd.DataFrame:
        df = pandas.DataFrame(columns=["Timestamp", "Connections"])
        df["Timestamp"] = self.__buffer["Timestamp"]
        df["Connections"] = self.__buffer["Connections"]
        return df

    def get_buffered_logs(self):
        return self.__buffer

    def get_running_since(self):
        return self.__format_sql_to_datetime(self.__db.running_since()[0][0])

    def get_logging_since(self):
        return self.__format_sql_to_datetime(self.__db.logging_since()[0][0])

    def buffer_empty(self):
        return self.__buffer.empty

    # for debugging only!!!
    def getDirectDbAccess(self):
        return self.__db


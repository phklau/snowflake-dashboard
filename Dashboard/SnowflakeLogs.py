import pandas

from SqliteDB import SqliteDB
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
        AND Error = 0"""
        logs = self.query_data(statement, (date_from.strftime("%Y-%m-%d %H:%M:%S"), date_till.strftime("%Y-%m-%d %H:%M:%S")))
        return logs
# Errors
# Down/Upstreams

# SnowFlakeLogs
class SnowflakeLogs:
    """
    API providing the required data for the dashboard
    """

    def __init__(self, pathtodb: str):
        self.__logging_since = None
        self.__running_since = None
        self.__db = SnowflakelogDB(pathtodb)
        self.__lastUpdate = datetime.now() - timedelta(hours=1)
        self.__buffer_from = None
        self.__buffer_till = None
        self.__buffer = pd.DataFrame()
        # querry all data on init and reload?
        if self.__db.is_db_connected():
            self.update_logging_since()
            self.update_running_since()
        else:
            raise Warning("Couldn't connect to db")

    def __query_data(self, date_from: datetime, date_till:datetime):
        if self.__buffer_update_needed(date_from, date_till):
            self.__buffer_from = date_from
            self.__buffer_till = date_till
            self.__lastUpdate = datetime.now()
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

    # if new data needed:
    # call def __get_logs_between
    # buffer as pandas/dict in class? querry only new when 1h + last timestamp?
    # connect time together
    # if grouping is needed (show whole week-->sum up to days), to it here
    # or https://plotly.com/python/time-series/ (Displaying Period Data)
    # https://datagy.io/pandas-datetime/

    # get_connections/errors/timestamps?
    def get_connections_between(self, date_from: datetime, date_till: datetime) -> pd.DataFrame:
        self.__query_data(date_from, date_till)
        df = pandas.DataFrame(columns=["Timestamp", "Connections"])
        df["Timestamp"] = self.__buffer["Timestamp"]
        df["Connections"] = self.__buffer["Connections"]
        return df

    def get_running_since(self):
        return self.__running_since

    def get_logging_since(self):
        return self.__logging_since

    def __buffer_update_needed(self, request_from: datetime, request_till: datetime) -> bool:
        result = False
        result &= self.__buffer_from != request_from
        result &= self.__buffer_till != request_till
        result &= (datetime.now() - self.__lastUpdate) >= timedelta(hours=1) # returns false!
        # return result
        return True

    # interface?
    # drawer object(fabric)
    # generates figures
    # instanciate with from till
    # table fabric

    # for debugging only!!!
    def getDirectDbAccess(self):
        return self.__db

    def __format_sql_to_datetime(self, timestamp: str) -> datetime:
        return datetime.strptime(timestamp, SnowflakelogDB.DATE_TIME_FORMAT)

    def update_running_since(self):
        self.__running_since = self.__format_sql_to_datetime(self.__db.running_since()[0][0])

    def update_logging_since(self):
        self.__logging_since = self.__format_sql_to_datetime(self.__db.logging_since()[0][0])

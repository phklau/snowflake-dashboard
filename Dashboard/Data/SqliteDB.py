import sqlite3


class SqliteDB:
    def __init__(self, pathtodb: str):
        try:
            self.__connection = sqlite3.connect(pathtodb)
            self.__connected = True
        except:
            self.__connected = False

    def __del__(self):
        self.__connection.close()

    def is_db_connected(self) -> bool:
        return self.__connected

    def close_connection(self):
        self.__connection.close()

    def query_data(self, statement, params: tuple = ()):
        """
        Querry data in the connected db
        :param statement: String with the statement
        :param params: Parameters of the querry
        :return: fetched data of sql query
        """
        if self.__connected:
            with self.__connection:
                c = self.__connection.cursor()
                try:
                    c.execute(statement, params)
                    data = c.fetchall()
                    c.close()
                    return data
                except:
                    return None
        else:
            return None

    def store_data(self, statement):
        """
        TODO: Implement this when using it also for the
        logToDb class
        :param statement:
        :return:
        """
        pass


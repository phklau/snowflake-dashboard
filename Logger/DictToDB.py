import sqlite3


class DictToDB:

    __connection = None
    __cursor = None
    __tableExists = False

    connected = False

    def __init__(self, pathToDb, tablestruct, tablename="logdata"):
        # Connect to DB
        try:
            self.__connection = sqlite3.connect(pathToDb)
        except:
            self.connected = False
        self.connected = True
        if self.connected:
            self.__cursor = self.__connection.cursor()
            # Check if Table exists
            try:
                with self.__connection:
                    self.__cursor.execute("""
                    CREATE TABLE {} (ID INTEGER PRIMARY KEY autoincrement)
                    """.format(tablename))
            except sqlite3.OperationalError:
                # DEBUG: print(sqlite3.OperationalError)
                self.__tableExists = True
            if not self.__tableExists:
                for key, type in tablestruct.items():
                    self.__cursor.execute("""
                    ALTER TABLE {} ADD {} {}
                    """.format(tablename, key, type))

    def __del__(self):
        self.__cursor.close()
        self.__connection.close()

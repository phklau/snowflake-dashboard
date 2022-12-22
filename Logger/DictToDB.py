import sqlite3


class DictToDB:

    __connection = None
    __cursor = None
    __tableExists = False
    __tableName = ""

    connected = False

    def __init__(self, pathToDb, sampleDict, tablename="logdata"):
        self.__tableName = tablename
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
                for key, sampledata in sampleDict.items():
                    if type(sampledata) == str:
                        dataType = "TEXT"
                    elif type(sampledata) == int:
                        dataType = "INTEGER"
                    elif type(sampledata) == float:
                        dataType = "REAL"
                    else:
                        dataType = "BLOB"
                    self.__cursor.execute("""
                    ALTER TABLE {} ADD {} {}
                    """.format(tablename, key, dataType))

    def __del__(self):
        self.__cursor.close()
        self.__connection.close()

    def writeDictInDb(self, data: dict):
        with self.__connection:
            # TODO: get rid of hardcoded stuff for more generic class
            self.__cursor.execute("""
            INSERT INTO {} VALUES 
            ( NULL,
             :Date, 
             :Time, 
             :Error, 
             :Errortype, 
             :ErrorDescription, 
             :Connections, 
             :Upload , 
             :Download)
            """.format(self.__tableName), data)

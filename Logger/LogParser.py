import re
from DictToDB import DictToDB


class LogParser:
    __db = None
    __m_data = {}
    __defaultData = {'Date': "",
                     'Time': "",
                     'Error': int(True),
                     'Errortype': "Sythax",
                     'ErrorDescription': "Doesn`t go overwritten",
                     'Connections': 0,
                     'Upload': 0.0,
                     'Download': 0.0}

    def __init__(self, pathToDb=r"./logs.sqlite"):
        self.__db = DictToDB(pathToDb, self.__defaultData)

    def toDict(self, logline):
        if self.__parseLog(logline):
            return self.__m_data
        else:
            return None

    def toDb(self, logline):
        if self.__parseLog(logline):
            self.__db.writeDictInDb(self.__m_data)
            return True
        else:
            return False

    def __parseLog(self, logline):
        self.__m_data = self.__defaultData.copy()
        self.__m_data['Date'] = re.search(r'[0-9]+\/[0-9]+\/[0-9]+', logline).group()
        self.__m_data['Time'] = re.search(r'\d{2}:\d{2}:\d{2}', logline).group()
        if re.search("ERROR", logline):
            self.__m_data['Error'] = int(True)
            try:
                self.__m_data['Errortype'] = re.search(r'\w+(?= ERROR)', logline).group()
                self.__m_data['ErrorDescription'] = re.search(r'(?<=\d{2}:\d{2}:\d{2} )[^\)]+', logline).group()
            except AttributeError:
                self.__m_data['Errortype'] = "Parser"
                self.__m_data['ErrorDescription'] = logline
        else:
            try:
                self.__m_data['Connections'] = int(re.search(r'\d+(?= connections.)', logline).group())
                uploadUnitScale = 1.0
                upload = re.search(r'\d+(?= MB,)', logline)
                if upload is None:
                    upload = re.search(r'\d+(?= KB,)', logline)
                    uploadUnitScale = 0.001
                    if upload is None:
                        upload = re.search(r'\d+(?= GB,)', logline)
                        uploadUnitScale = 1000
                self.__m_data['Upload'] = int(upload.group()) * uploadUnitScale  # TODO: Test conversions with debugger
                downloadUnitScale = 1.0
                download = re.search(r'\d+(?= MB\.)', logline)
                if download is None:
                    download = re.search(r'\d+(?= KB\.)', logline)
                    downloadUnitScale = 0.001
                    if download is None:
                        download = re.search(r'\d+(?= GB\.)', logline)
                        downloadUnitScale = 1000
                self.__m_data['Download'] = int(download.group()) * downloadUnitScale
                self.__m_data['Error'] = int(False)
                self.__m_data['Errortype'] = ""
                self.__m_data['ErrorDescription'] = ""
            except AttributeError:
                self.__m_data['Errortype'] = "Parser"
                self.__m_data['ErrorDescription'] = logline
        return bool(self.__m_data != self.__defaultData)

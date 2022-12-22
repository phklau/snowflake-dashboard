import re


class LogParser:
    __m_data = {}
    __defaultData = {'Date': "",
                     'Time': "",
                     'Error': int(True),
                     'Errortype': "Sythax",
                     'ErrorDescription': "Doesn`t go overwritten",
                     'Connections': 0,
                     'Upload': 0,
                     'Download': 0}

    def toDict(self, logline):
        if self.__parseLog(logline):
            return self.__m_data
        else:
            return None

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
                self.__m_data['Upload'] = int(re.search(r'\d+(?= MB,)', logline).group())
                self.__m_data['Download'] = int(re.search(r'\d+(?= MB.)', logline).group())
                self.__m_data['Error'] = int(False)
                self.__m_data['Errortype'] = ""
                self.__m_data['ErrorDescription'] = ""
            except AttributeError:
                self.__m_data['Errortype'] = "Parser"
                self.__m_data['ErrorDescription'] = logline
        return bool(self.__m_data != self.__defaultData)

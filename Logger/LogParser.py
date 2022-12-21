import re

class LogParser:
    __m_data = {}
    dataLogged = False

    def getData(self):
        if not self.dataLogged:
            # Writeinto Error? But whole error handling is happening in parseLog?
            print(self.dataLogged)
        return self.__m_data
    def parseLog(self, logline):
        date = ""
        time = ""
        connections = 0
        upload = 0
        download = 0
        error = True
        errorType = "Sythax"
        errorDiscription = "Doesn't got overwritten"

        self.__m_data = {}

        date = re.search(r'[0-9]+\/[0-9]+\/[0-9]+', logline).group()
        time = re.search(r'\d{2}:\d{2}:\d{2}', logline).group()
        if re.search("ERROR", logline):
           error = True
           try:
               errorType = re.search(r'\w+(?= ERROR)', logline).group()
               errorDiscription = re.search(r'(?<=\d{2}:\d{2}:\d{2} )[^\)]+', logline).group()
           except AttributeError:
               errorType = "Parser"
               errorDiscription = logline
        else:
            try:
                connections = re.search(r'\d+(?= connections.)', logline).group()
                upload = re.search(r'\d+(?= MB,)', logline).group()
                download = re.search(r'\d+(?= MB.)', logline).group()
                error = False
                errorType = ""
                errorDiscription = ""
            except AttributeError:
                error = True
                errorType = "Parser"
                errorDiscription = logline
            self.__m_data.update({"Connections": connections,
                                "Upload": upload,
                                "Download": download,
                                  })
        # append date time error
        self.__m_data.update({
                            "Date": date,
                            "Time": time,
                            "Error": error,
                            "Errortype": errorType,
                            "Error discription": errorDiscription
                              })
        self.dataLogged = bool(self.__m_data != {})

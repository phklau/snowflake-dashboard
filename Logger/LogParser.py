import abc
import datetime
import re
from DictToDB import DictToDB


class AbstractLogParser(abc.ABC):

    def __init__(self, pathToDb=r"./logs.sqlite"):
        self.__db = None
        self.__m_data = {}
        self.__defaultData = {'Timestamp': "",
                              'Error': int(True),
                              'Errortype': "Sythax",
                              'Details': "Doesn`t got overwritten",
                              'Connections': 0,
                              'Upload': 0.0,
                              'Download': 0.0}
        self.__db = DictToDB(pathToDb, self.__defaultData)

    def toDict(self, logline):
        if self._parse_log(logline):
            return self.__m_data
        else:
            return None

    def toDb(self, logline):
        if self._parse_log(logline):
            self.__db.writeDictInDb(self.__m_data)
            return True
        else:
            return False

    def _get_log_time_format(self) -> str:
        return "%Y/%m/%d %H:%M:%S"

    def _get_db_time_format(self) -> str:
        return "%Y-%m-%d %H:%M:%S"

    @abc.abstractmethod
    def _parse_timestamp(self, logline: str) -> int:
        raise NotImplementedError

    @abc.abstractmethod
    def _parse_connections(self, logline: str) -> int:
        raise NotImplementedError

    """
    Must implement handling for different data units in the logline
    Returns:
        float: upload data in line of the log in Mb
    """
    @abc.abstractmethod
    def _parse_upload_mb(self, logline: str) -> float:
        raise NotImplementedError

    """
    Must implement handling for different data units in the logline
    Returns:
        float: download data in line of the log in Mb
    """
    @abc.abstractmethod
    def _parse_download_mb(self, logline: str) -> float:
        raise NotImplementedError

    @abc.abstractmethod
    def _parse_startup_details(self, logline: str) -> str:
        raise NotImplementedError

    @abc.abstractmethod
    def _parse_error_type(self, logline: str) -> str:
        raise NotImplementedError

    @abc.abstractmethod
    def _parse_error_details(self, logline: str) -> str:
        raise NotImplementedError

    @abc.abstractmethod
    def _is_connection_data(self, logline: str) -> bool:
        raise NotImplementedError

    @abc.abstractmethod
    def _is_error(self, logline: str) -> bool:
        raise NotImplementedError

    @abc.abstractmethod
    def _is_startup(self, logline: str) -> bool:
        raise NotImplementedError

    def _parse_log(self, logline):
        self.__m_data = self.__defaultData.copy()
        raw_timestamp = self._parse_timestamp(logline)
        raw_date_time = datetime.datetime.strptime(raw_timestamp, self._get_log_time_format())
        self.__m_data['Timestamp'] = raw_date_time.strftime(self._get_db_time_format())
        if self._is_connection_data(logline):
            try:
                self.__m_data['Connections'] = self._parse_connections(logline)
                self.__m_data['Upload'] = self._parse_upload_mb(logline)
                self.__m_data['Download'] = self._parse_download_mb(logline)
                self.__m_data['Error'] = int(False)
                self.__m_data['Errortype'] = ""
                self.__m_data['Details'] = ""
            except AttributeError:
                self.__m_data['Errortype'] = "Parser"
                self.__m_data['Details'] = logline
        elif self._is_startup(logline):
            self.__m_data['Error'] = int(False)
            self.__m_data['Details'] = self._parse_startup_details(logline)
            self.__m_data['Errortype'] = ""
        if re.search("ERROR", logline):
            self.__m_data['Error'] = int(True)
            try:
                self.__m_data['Errortype'] = self._parse_error_type(logline)
                self.__m_data['Details'] = self._parse_error_details(logline)
            except AttributeError:
                self.__m_data['Errortype'] = "Parser"
                self.__m_data['Details'] = logline
        return bool(self.__m_data != self.__defaultData)


class LogParserTillV2_8_0(AbstractLogParser):

    def _parse_timestamp(self, logline: str) -> str:
        return re.search(r'\d{4}\/\d{2}\/\d{2} \d{2}:\d{2}:\d{2}', logline).group()

    def _parse_connections(self, logline: str) -> int:
        return int(re.search(r'\d+(?= connections.)', logline).group())

    def _parse_upload_mb(self, logline: str) -> float:
        unit_scale = 0.001
        upload = re.search(r'\d+(?= KB,)', logline)
        return int(upload.group()) * unit_scale

    def _parse_download_mb(self, logline: str) -> float:
        unit_scale = 0.001
        download = re.search(r'\d+(?= KB\.)', logline)
        return int(download.group()) * unit_scale

    def _parse_startup_details(self, logline: str) -> str:
        return re.search(r'(?<=\d{2}:\d{2}:\d{2} ).+', logline).group()

    def _parse_error_type(self, logline: str) -> str:
        return re.search(r'\w+(?= ERROR)', logline).group()

    def _parse_error_details(self, logline: str) -> str:
        return re.search(r'(?<=\d{2}:\d{2}:\d{2} )[^\)]+', logline).group()

    def _is_connection_data(self, logline: str) -> bool:
        return re.search("connections", logline) is not None

    def _is_error(self, logline: str) -> bool:
        return re.search("ERROR", logline) is not None

    def _is_startup(self, logline: str) -> bool:
        return re.search("Proxy starting", logline) is not None or re.search("NAT type:", logline) is not None

#!/usr/bin/env python3
import json
from pathlib import Path

from LogParser import LogParser
import fileinput

debug = True
if debug:
    DB_PATH = "./snowflakelogs.sqlite"
    LOGFILE_PATH = "./snowflakelogs_lowerV2-8-0.log"
else:
    with open(Path(__file__).parent.parent.joinpath("Settings/logger.json")) as settings_json:
        settings = json.load(settings_json)
    DB_PATH = settings["Path to database"]
    LOGFILE_PATH = settings["Path to logfile"]
    STORE_IN_FILE_TOO = settings["Store logs in file"]

if __name__ == "__main__":
    parser = LogParser(DB_PATH)
    if debug:
        logfileLocation = LOGFILE_PATH
        with open(logfileLocation) as file:
            content = file.readlines()
        for line in content:
            print(parser.toDict(line))
            print(parser.toDb(line))
    else:
        with fileinput.input() as f_input:
            for line in f_input:
                parser.toDb(line)
                # write still into logfile
                if STORE_IN_FILE_TOO:
                    with open(LOGFILE_PATH, "a") as logfile:
                        logfile.write(line)


#!/usr/bin/env python3

from LogParser import LogParser
import fileinput
import json

debug = False

with open("../Settings/logger.json") as settings_json:
    settings = json.load(settings_json)
DB_PATH = settings["Path to database"]
LOGFILE_PATH = settings["Path to logfile"]
STORE_IN_FILE_TOO = settings["Store logs in file"]

if __name__ == "__main__":
    parser = LogParser(DB_PATH)
    if debug:
        logfileLocation = "./logexmp.log"
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


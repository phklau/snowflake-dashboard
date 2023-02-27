#!/usr/bin/env python3

from LogParser import LogParser
import fileinput
debug = False

DB_PATH = r"./snowflakelogs.sqlite"
DEBUGLOGFILE_PATH = r"./snowflakelogs.log"

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
                parser.toDb(DB_PATH)
                # write still into logfile
                with open(DEBUGLOGFILE_PATH, "a") as logfile:
                    logfile.write(line)


#!/usr/bin/env python3

from LogParser import LogParser
import fileinput
debug = True

if __name__ == "__main__":
    parser = LogParser()
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

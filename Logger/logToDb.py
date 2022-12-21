#!/usr/bin/env python3

from LogParser import LogParser
import fileinput

if __name__ == "__main__":
    parser = LogParser()
    with fileinput.input() as f_input:
        for line in f_input:
            parser.parseLog(line)
            print(parser.getData())  # change to write in DB

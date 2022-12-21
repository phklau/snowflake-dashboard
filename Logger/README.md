# Logger Module

The logger parses the string from snowflake to a database.
Logs are read in via piped stdout/err from snowflake app.

## Architecture:

Main(logToDb.py):
- read fileinput

Parser Class(LogParser.py)
- toDict
  call parseLog
  return dict
- parse
  - Timestamp
  - Connections
  - Upload
  - Download
  - Errors
  will be parsed out of the input string into the private member dict
- write in DB

DictToDBManger
__init__(path, dict-keys):
- set path to SQLite Db
- connect
- check if Table needs to be created

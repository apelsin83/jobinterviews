# WAES - tool for comparing base64 encoded binary data


## Requirements

- python 2.7.*
- pip

## Installation

 - create virtual enviroment
 - install dependencies 

 ```
 pip install -r requirements.txt
 ```

## Features

- multithreading is implemented with gevent library

- Endpoints accept JSON base64 encoded binary data
 ```
 <host>/v1/diff/<ID>/left
 <host>/v1/diff/<ID>/right
```

JSON structure

```
{'payload': 'encoded data'}
```
Also required header:

Content-Type: application/json
ID should be integer


- Endpoint return difference between 2 datas left and right
```
<host>/v1/diff/<ID>
```
Response 
```
{'payload': 'Different length'}
{'payload': 'Equal'}
{'payload': [
              {'offset': XXX, 'length': XXX},
              {'offset': XXX, 'length': XXX}...
             ]}
```

## Program logic

### Program is separated for several levels:

- part responsible for reciving request 
- business logic. Checks input data and provides comparison process
- data layer. 

### DataLayer
Because the storage was not specified was created top level object DataLayer which can be initiated with different storages types.

DataLayer has 3 methods:
- init_db - accepts instance of storage of your choice which implements interface BaseDbInterface. Examples in data/file_db.py and stub in data/mysql_db.py

- save - save data to storage

- get - return data from storage
 
### File db storage written without unit test (lack of time)
I implemented simple file db storage. With several features:

- data is stored in folder with name ID_left or ID_right
- during read/create/update process files are locked

Lock mechanism:
- before create/update/read I create folder with name ID_left.lock or ID_right.lock
- if create folder failed user receives error message
- if folder created - inside I put lock file with current timestamp
- when process create/update/read is finished I remove folder
- to prevent file locking forever because of crashes there is a background process which checks files with timestamp inside locking folders and delete them if they were expired.


## Local Development

```
python main.py
```

## Server run under gunicorn

```
gunicorn -b 0.0.0.0:8088 -k gevent -w 4 wsgi:application 
```

For prodction/other enviroment all settings could be overritten in local_settings.py

## Unit and functional Tests

```
python -m unittest discover .
```

## Coverage tests with report

- coverage run -m unittest discover 
- coverage html


## Settings to manage application:

DEBUG - is debug mode enabled

LOG_FILE - log file location

SERVER - ip to run server

PORT - port to run server

FILE_DB_SETTINGS - settings for file storage

TTL_LOCK  - number of seconds that file can be locked

SLEEP_CHECK - period in seconds when clean thread check stacked updated files

MEMFILE_MAX - Maximum size of memory buffer for body request in bytes.


## Suggestions for improvement:

- after first diff we can store result and keep it until next data update

- to speed up comparison process. When we receive data we: 
  - build hash of this data for example md5 or sha-512
  - data length

  and store result separately. When we receive request for diff we first check length then hash. If lengths are equal and hash differs we check data for difference

- if data is very big. It could be splitted for chunks during processing

- if high speed is very important after request with posted encoded data we can start background task which check data if both available and store result which we read

- improve locking for file_db storage

- use instead my file storage regular db which suits for this purposes.


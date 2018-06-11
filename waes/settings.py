DEBUG = True
LOG_FILE = './waes.log'
SERVER = '127.0.0.1'
PORT = '8088'
FILE_DB_SETTINGS = {
    'folder': './dbfiles'
}
TTL_LOCK = 5
SLEEP_CHECK = 1
MEMFILE_MAX = 102400


try:
    from local_settings import *
except ImportError:
    pass

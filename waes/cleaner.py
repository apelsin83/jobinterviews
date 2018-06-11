import gevent
import time
import os
import shutil
from logging import getLogger
from settings import TTL_LOCK, SLEEP_CHECK, FILE_DB_SETTINGS

logger = getLogger('waes')


def clear_loop(location):
    # Clear stucked files
    while True:
        try:
            clear(location, TTL_LOCK)
            gevent.sleep(SLEEP_CHECK)
        except Exception as ex:
            logger.error(str(ex), exc_info=True)


def clear(location, ttl):
    tm = time.time()
    # scan for lock folders
    folders = [os.path.join(location, i) for i in os.listdir(location)
               if os.path.isdir(os.path.join(location, i)) and 'lock' in i]
    if folders:
        for f in folders:
            # check timestamp in file if expired - remove folder
            fname = os.path.join(f, 'lock')
            try:
                with open(fname, 'rb') as df:
                    data = df.read()
                tm_in_file = float(data)
                if tm - tm_in_file > ttl:
                    shutil.rmtree(f)
            except Exception as ex:
                logger.error(str(ex), exc_info=True)

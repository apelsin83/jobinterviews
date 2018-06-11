import gevent.monkey
gevent.monkey.patch_all()


# setup bottle
from settings import DEBUG, MEMFILE_MAX
import bottle
bottle.BaseRequest.MEMFILE_MAX = MEMFILE_MAX

# Setup logger
import logging
from shared.logger import setup_logger
from settings import LOG_FILE, SERVER, PORT
setup_logger('waes', LOG_FILE, logging.DEBUG)

# Init storage settings
from settings import FILE_DB_SETTINGS
from data.data_layer import DataLayer
from data.file_db import FileDb

fileDb = FileDb(**FILE_DB_SETTINGS)
dl = DataLayer()
dl.init_db(fileDb)

# Load the url mappings
import api

# Create a WSGI app
app = application = bottle.default_app()


if __name__ == '__main__':
    # bottle.run(host='127.0.0.1', port=8088, debug=DEBUG, reloader=True)
    bottle.run(host=SERVER, port=PORT, debug=DEBUG, server='gevent')

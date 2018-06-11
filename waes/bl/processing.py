import json
from data.data_layer import DataLayer
from logging import getLogger

logger = getLogger('waes')


def check_request(req, id):
    if not str(id).isdigit():
        err = 'Id should be a integer'
    else:
        json_header = req.headers.get('Content-Type')
        err = ''
        if not json_header or json_header != "application/json":
            err = 'Request should contains header: Content-Type: application/json'
        else:
            request_json = req.json
            if not request_json or 'payload' not in request_json.keys():
                err = 'Wrong json structure: {payload: xxx}'
            else:
                return True, request_json["payload"]
    logger.debug(err)
    return False, {'error': err}


def save_file(id, side, data, data_layer=''):
    dl = data_layer if data_layer else DataLayer()
    dl.save(id, side, data)

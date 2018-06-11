import json
import base64
from bottle import request, post, get, route, put, HTTPResponse
from logging import getLogger
from bl.comparison import compare_files
from bl.processing import save_file, check_request

logger = getLogger('waes')


@post('/v1/diff/<id>/left')
@post('/v1/diff/<id>/right')
@put('/v1/diff/<id>/left')
@put('/v1/diff/<id>/right')
def save_data(id):
    is_ok, data = check_request(request, id)
    if not is_ok:
        return HTTPResponse(data, 400)
    side = request.url.split('/')[-1]
    try:
        save_file(id, side, data)
    except OSError as ex:
        return HTTPResponse({'error': str(ex)}, 400)
    return HTTPResponse(status=200)


@get('/v1/diff/<id>')
def diff(id):
    try:
        return compare_files(id)
    except IOError as ex:
        return HTTPResponse({'error': str(ex)}, 400)


@route('/<url:re:.*>')
def main(url):
    return HTTPResponse(status=403)

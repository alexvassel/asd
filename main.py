# -*- coding: utf-8 -*-
from StringIO import StringIO
from httplib import BAD_REQUEST

from bottle import run, request, post, HTTPError, BaseRequest

from helpers import Processor, POST_PARAM_NAME, ALLOWED_ACTIONS


# Ограничение bottle на тело запроса
BaseRequest.MEMFILE_MAX = 1024 * 1024


@post('/process/<action>/')
def process(action):
    if request.params.keys() != [POST_PARAM_NAME] or action not in ALLOWED_ACTIONS:
        raise HTTPError(BAD_REQUEST)

    string = request.params[POST_PARAM_NAME]

    compressor = Processor(StringIO(string))

    # IOError означает, что Processor получил для обработки не bz2 строку
    try:
        for block in getattr(compressor, action)():
            yield block
    except IOError:
        raise HTTPError(BAD_REQUEST)

run(host='localhost', port=8080)

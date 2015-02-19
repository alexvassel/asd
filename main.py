# -*- coding: utf-8 -*-
from StringIO import StringIO
from httplib import BAD_REQUEST

from bottle import run, request, post, HTTPError, BaseRequest, response

from helpers import Processor, POST_PARAM_NAME, Action


# Ограничение bottle на тело запроса
BaseRequest.MEMFILE_MAX = 1024 * 1024


@post('/process/<action>/')
def process(action):
    if POST_PARAM_NAME not in request.params or action not in Action.allowed:
        raise HTTPError(BAD_REQUEST)

    string = request.params[POST_PARAM_NAME]

    processor = Processor(StringIO(string), action)

    response.content_type = ('text/plain' if action == Action.DECOMPRESS
                             else ' application/x-bzip2')

    # IOError означает, что Processor получил для обработки не bz2 строку
    try:
        for block in processor.process():
            yield block
    except IOError:
        raise HTTPError(BAD_REQUEST)

run(host='localhost', port=8080)

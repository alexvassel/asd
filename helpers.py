# -*- coding: utf-8 -*-

import bz2

POST_PARAM_NAME = 'string'


# Available request actions
class Action:
    COMPRESS = 'compress'
    DECOMPRESS = 'decompress'

    allowed = (COMPRESS, DECOMPRESS)


class Processor(object):
    """
    Compress/decompress of a file-like object content
    """

    CHUNK_SIZE = 32

    def __init__(self, buffer_object, action):
        self.buffer = buffer_object
        self.action = action

    def process(self):
        """
        Compression/decompression
        """
        processor = (bz2.BZ2Compressor() if self.action == Action.COMPRESS
                     else bz2.BZ2Decompressor())

        # Выбираем метод в зависимости от действия
        action = getattr(processor, self.action)

        # Reading request and responding by chunks
        while True:
            block = self.buffer.read(self.CHUNK_SIZE)
            if not block:
                break
            # Actual compression/decompression
            processed = action(block)

            if processed:
                yield processed

        # Flush compression buffer
        if self.action == Action.COMPRESS:
            yield processor.flush()

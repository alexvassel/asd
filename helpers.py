# -*- coding: utf-8 -*-

import bz2

# Имя POST параметра
POST_PARAM_NAME = 'string'

# Доступные действия
ALLOWED_ACTIONS = ('compress', 'decompress')


class Processor(object):
    """
    Класс для архивирования, разархивирования строк
    Принимает в конструкторе объект, который предоставляет методы, характерные для файла
    """

    # Размер чанка
    CHUNK_SIZE = 32

    def __init__(self, file_object, action):
        self.buffer = file_object
        self.action = action

    def process(self):
        """
        архивирование
        """
        processor = self.processor

        # Читаем и отдаем содержимое запроса чанками
        while True:
            block = self.buffer.read(self.CHUNK_SIZE)
            if not block:
                break
            # Архивация/разархивация
            processed = getattr(processor, self.action)(block)

            if processed:
                yield processed

        # Очистить буфер в случае архивации
        if self.action == ALLOWED_ACTIONS[0]:
            yield processor.flush()

    @property
    def processor(self):
        return bz2.BZ2Compressor() if self.action == ALLOWED_ACTIONS[0] else bz2.BZ2Decompressor()

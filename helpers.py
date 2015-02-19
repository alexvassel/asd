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

    # Размер чанка для чтения
    CHUNK_SIZE = 32

    def __init__(self, file_object):
        self.buffer = file_object

    def compress(self):
        """
        архивирование
        """
        compressor = bz2.BZ2Compressor()

        # Читаем и файлоподобный объект чанками
        while True:
            block = self.buffer.read(self.CHUNK_SIZE)
            if not block:
                break
            compressor.compress(block)

        # Завершение процесса архивирования
        response = compressor.flush()

        # Отдаем чанками
        while response:
            to_send = response[:self.CHUNK_SIZE]
            response = response[self.CHUNK_SIZE:]
            yield to_send

    def decompress(self):
        """
        разархивирование
        """
        decompressor = bz2.BZ2Decompressor()

        # Читаем и разархивируем и отдаем строку чанками
        while True:
            block = self.buffer.read(self.CHUNK_SIZE)
            if not block:
                break
            processed = decompressor.decompress(block)

            if processed:
                yield processed

# SPDX-License-Identifier: MIT
# SPDX-FileCopyrightText: Sven Eckelmann <sven@narfation.org>

import math
from .chunk import Chunk
from .ecc import EccMeta
from .ecc import EccBch
from .ecc import EccRs
from .ecc import EccType


__all__ = [
    'Page',
]


class Page:
    __data = None  # type: bytes
    __ecc_codec = None  # type: EccMeta

    def __init__(self, page_size: int = 2048, oob_size: int = 64,
                 widebus: bool = False, ecc=EccType.BCH4) -> None:
        self.__page_size = page_size
        self.__oob_size = oob_size
        self.__widebus = widebus
        self.__ecc = ecc

        if self.__ecc == EccType.RS:
            self.__ecc_codec = EccRs()
        elif self.__ecc == EccType.RS_SBL:
            self.__ecc_codec = EccRs()
        elif self.__ecc == EccType.BCH4:
            self.__ecc_codec = EccBch(4)
        elif self.__ecc == EccType.BCH8:
            self.__ecc_codec = EccBch(8)
        else:
            raise ValueError("ecc invalid")

        self.__chunk = Chunk(self.__ecc_codec, ecc=self.__ecc,
                             page_size=self.__page_size,
                             widebus=self.__widebus)

        no_chunks = math.ceil(self.__page_size / self.__chunk.data_size)
        required_size = no_chunks * self.__chunk.size
        if required_size > self.__page_size + self.__oob_size:
            raise ValueError("ECC needs more than available OOB size")

    def program(self, data: bytes) -> bytes:
        if len(data) < self.__page_size:
            needed_padding = self.__page_size - len(data)
            data += b'\x00' * needed_padding

        self.__data = self.__prepare_qca_page(data)

        return self.__data

    def __prepare_qca_page(self, data) -> bytes:
        page_parts = []

        # split data in smaller portions and convert it to chunks
        page_size = 0
        for i in range(0, len(data), self.__chunk.data_size):
            chunk_data = data[i:i+self.__chunk.data_size]
            self.__chunk.program(chunk_data)
            page_parts.append(self.__chunk.data)
            page_size += self.__chunk.size

        # ensure that the page is completely filled
        if page_size < self.__page_size + self.__oob_size:
            needed_padding = self.__page_size + self.__oob_size - page_size
            page_parts.append(b'\xff' * needed_padding)

        return b''.join(page_parts)

    @property
    def data(self) -> bytes:
        return self.__data

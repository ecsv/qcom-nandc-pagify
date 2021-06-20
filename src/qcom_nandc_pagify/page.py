# SPDX-License-Identifier: MIT
# SPDX-FileCopyrightText: Sven Eckelmann <sven@narfation.org>

import math
from .chunk import Chunk
from .ecc import ECC_Meta
from .ecc import ECC_BCH
from .ecc import ECC_RS
from .ecc import ECC_Type


__all__ = 'Page',


class Page:
    __data = None  # type: bytes
    __ecc_codec = None  # type: ECC_Meta

    def __init__(self, page_size: int = 2048, oob_size: int = 64,
                 widebus: bool = False, ecc=ECC_Type.BCH4) -> None:
        self.__page_size = page_size
        self.__oob_size = oob_size
        self.__widebus = widebus
        self.__ecc = ecc

        if self.__ecc == ECC_Type.RS:
            self.__ecc_codec = ECC_RS()
        elif self.__ecc == ECC_Type.RS_SBL:
            self.__ecc_codec = ECC_RS()
        elif self.__ecc == ECC_Type.BCH4:
            self.__ecc_codec = ECC_BCH(4)
        elif self.__ecc == ECC_Type.BCH8:
            self.__ecc_codec = ECC_BCH(8)
        else:
            raise ValueError("ecc invalid")

        self.__chunk = Chunk(self.__ecc_codec, ecc=self.__ecc,
                             page_size=self.__page_size,
                             widebus=self.__widebus)

    def program(self, data: bytes) -> None:
        if len(data) < self.__page_size:
            needed_padding = self.__page_size - len(data)
            data += b'\x00' * needed_padding

        self.__data = self.__prepare_qca_page(data)

    def __prepare_qca_page(self, data) -> bytes:
        page_parts = []

        no_chunks = math.ceil(self.__page_size / self.__chunk.codeword_size)
        required_size = no_chunks * self.__chunk.size
        if required_size > self.__page_size + self.__oob_size:
            raise ValueError("ECC needs more than available OOB size")

        # split data in smaller codewords and convert it to chunks
        page_size = 0
        for i in range(0, len(data), self.__chunk.codeword_size):
            codeword = data[i:i+self.__chunk.codeword_size]
            self.__chunk.program(codeword)
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

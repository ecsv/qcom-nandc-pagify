# SPDX-License-Identifier: MIT
# SPDX-FileCopyrightText: Sven Eckelmann <sven@narfation.org>

from .ecc import ECC_Type, ECC_Meta

__all__ = 'Chunk',


class Chunk:
    __data = None  # type: bytes
    __ecc_codec = None  # type: ECC_Meta

    def __init__(self, ecc_codec: ECC_Meta, ecc=ECC_Type.BCH4,
                 page_size: int = 2048, widebus: bool = False) -> None:
        self.__ecc = ecc
        self.__ecc_codec = ecc_codec
        self.__widebus = widebus

        if self.__widebus:
            self.__bbm_size = 2
        else:
            self.__bbm_size = 1

        if self.__ecc == ECC_Type.RS:
            self.__codeword_size = 516
            self.__oob_per_chunk = 12
        elif self.__ecc == ECC_Type.RS_SBL:
            self.__codeword_size = 512
            self.__oob_per_chunk = 16
        elif self.__ecc == ECC_Type.BCH4:
            self.__codeword_size = 516
            self.__oob_per_chunk = 12
        elif self.__ecc == ECC_Type.BCH8:
            self.__codeword_size = 516
            self.__oob_per_chunk = 16
        else:
            raise ValueError("ecc invalid")

        self.__bbm_pos = page_size % self.size

    def program(self, codeword: bytes) -> None:
        # read a full codeword and add necessary padding
        if len(codeword) < self.__codeword_size:
            needed_padding = self.__codeword_size - len(codeword)
            codeword += b'\xff' * needed_padding

        self.__data = self.__prepare_qca_chunk(codeword)

    def __prepare_qca_chunk(self, codeword: bytes) -> bytes:
        ecc = self.__ecc_codec.encode(codeword)

        chunk_parts = [
            codeword[0:self.__bbm_pos],
            b'\xff' * self.__bbm_size,
            codeword[self.__bbm_pos:self.__codeword_size],
            ecc,
            b'\xff' * (self.__oob_per_chunk - len(ecc) - self.__bbm_size),
        ]

        return b''.join(chunk_parts)

    @property
    def data(self) -> bytes:
        return self.__data

    @property
    def size(self) -> int:
        return self.__codeword_size + self.__oob_per_chunk

    @property
    def codeword_size(self) -> int:
        return self.__codeword_size

    @property
    def oob_size(self) -> int:
        return self.__oob_per_chunk

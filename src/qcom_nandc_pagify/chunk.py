# SPDX-License-Identifier: MIT
# SPDX-FileCopyrightText: Sven Eckelmann <sven@narfation.org>

from .ecc import EccType, EccMeta

__all__ = [
    'Chunk',
]


class Chunk:
    __data = None  # type: bytes
    __ecc_codec = None  # type: EccMeta

    def __init__(self, ecc_codec: EccMeta, ecc=EccType.BCH4,
                 page_size: int = 2048, widebus: bool = False) -> None:
        self.__ecc = ecc
        self.__ecc_codec = ecc_codec
        self.__widebus = widebus

        if self.__widebus:
            self.__bbm_size = 2
        else:
            self.__bbm_size = 1

        if self.__ecc == EccType.RS:
            self.__data_size = 516
            self.__oob_per_chunk = 12
        elif self.__ecc == EccType.RS_SBL:
            self.__data_size = 512
            self.__oob_per_chunk = 16
        elif self.__ecc == EccType.BCH4:
            self.__data_size = 516
            self.__oob_per_chunk = 12
        elif self.__ecc == EccType.BCH8:
            self.__data_size = 516
            self.__oob_per_chunk = 16
        else:
            raise ValueError("ecc invalid")

        self.__bbm_pos = page_size % self.size

    def program(self, data: bytes) -> bytes:
        # read a full data portion and add necessary padding
        if len(data) < self.__data_size:
            needed_padding = self.__data_size - len(data)
            data += b'\xff' * needed_padding

        self.__data = self.__prepare_qca_chunk(data)

        return self.__data

    def __prepare_qca_chunk(self, data: bytes) -> bytes:
        ecc = self.__ecc_codec.encode(data)

        chunk_parts = [
            data[0:self.__bbm_pos],
            b'\xff' * self.__bbm_size,
            data[self.__bbm_pos:self.__data_size],
            ecc,
            b'\xff' * (self.__oob_per_chunk - len(ecc) - self.__bbm_size),
        ]

        return b''.join(chunk_parts)

    @property
    def data(self) -> bytes:
        return self.__data

    @property
    def size(self) -> int:
        return self.__data_size + self.__oob_per_chunk

    @property
    def data_size(self) -> int:
        return self.__data_size

    @property
    def oob_size(self) -> int:
        return self.__oob_per_chunk

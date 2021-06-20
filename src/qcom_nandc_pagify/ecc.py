# SPDX-License-Identifier: MIT
# SPDX-FileCopyrightText: Sven Eckelmann <sven@narfation.org>

import math
import bchlib
import reedsolo as rs
from enum import Enum
from abc import ABCMeta, abstractmethod

__all__ = (
    'ECC_Type',
    'ECC_BCH',
    'ECC_RS',
)


class ECC_Type(Enum):
    RS = 1
    RS_SBL = 2
    BCH4 = 3
    BCH8 = 4


class ECC_Meta(metaclass=ABCMeta):
    @abstractmethod
    def encode(self, data: bytes) -> bytes:
        pass

    @property
    @abstractmethod
    def size(self) -> int:
        pass


class ECC_BCH(ECC_Meta):
    def __init__(self, bits: int = 4) -> None:
        self.__bits = bits
        self.__bch = bchlib.BCH(8219, bits)

    def encode(self, data: bytes) -> bytes:
        return self.__bch.encode(data)

    @property
    def size(self) -> int:
        return int(math.ceil(self.__bits * 13 / 8))


class ECC_RS(ECC_Meta):
    def __init__(self) -> None:
        rs.init_tables(c_exp=10, prim=0x409)
        self.__gen = rs.rs_generator_poly(8, fcr=1)

    def encode(self, data: bytes) -> bytes:
        if len(data) > 1015:
            raise ValueError('ECC data larger than 1015 bytes')

        padded_data = b'\x00' * (1015 - len(data)) + data
        array_data = [x for x in padded_data]
        eccpre = rs.rs_encode_msg(array_data, 8, gen=self.__gen)[1015:]

        eccbytes = []
        pos = 0
        for i in range(0, 10):
            relpos = i % 5
            if relpos != 0:
                pos += 1

            v = 0

            shift_cur_byte = 2 * relpos
            if shift_cur_byte != 8:
                v += eccpre[pos] << shift_cur_byte

            shift_last_byte = 10 - 2 * relpos
            if shift_last_byte != 10:
                v += eccpre[pos - 1] >> shift_last_byte

            v &= 0xff
            eccbytes.append(v)

        return bytes(eccbytes)

    @property
    def size(self) -> int:
        return 10

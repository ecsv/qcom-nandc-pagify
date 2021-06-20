# SPDX-License-Identifier: MIT
# SPDX-FileCopyrightText: Sven Eckelmann <sven@narfation.org>

from dataclasses import dataclass
from unittest import TestCase
from src.qcom_nandc_pagify import Page
from src.qcom_nandc_pagify import EccType


@dataclass
class TestConfig:
    raw: str
    page: str
    page_size: int
    oob_size: int
    ecc: EccType = EccType.BCH4
    widebus: bool = False  # TODO


class ConfigTestCase(TestCase):
    def test_page(self):
        configs = [
            # RS, 2k+64
            TestConfig(raw='zero',    page='zero_rs',      page_size=2048,
                       ecc=EccType.RS,     oob_size=64),
            TestConfig(raw='random1', page='random1_rs',   page_size=2048,
                       ecc=EccType.RS,     oob_size=64),
            TestConfig(raw='random2', page='random2_rs',   page_size=2048,
                       ecc=EccType.RS,     oob_size=64),
            TestConfig(raw='random3', page='random3_rs',   page_size=2048,
                       ecc=EccType.RS,     oob_size=64),
            TestConfig(raw='random4', page='random4_rs',   page_size=2048,
                       ecc=EccType.RS,     oob_size=64),
            TestConfig(raw='random5', page='random5_rs',   page_size=2048,
                       ecc=EccType.RS,     oob_size=64),
            TestConfig(raw='ff',      page='ff_rs',        page_size=2048,
                       ecc=EccType.RS,     oob_size=64),

            # RS, 2k+128
            TestConfig(raw='zero',    page='zero_rs',      page_size=2048,
                       ecc=EccType.RS,     oob_size=128),
            TestConfig(raw='random1', page='random1_rs',   page_size=2048,
                       ecc=EccType.RS,     oob_size=128),
            TestConfig(raw='random2', page='random2_rs',   page_size=2048,
                       ecc=EccType.RS,     oob_size=128),
            TestConfig(raw='random3', page='random3_rs',   page_size=2048,
                       ecc=EccType.RS,     oob_size=128),
            TestConfig(raw='random4', page='random4_rs',   page_size=2048,
                       ecc=EccType.RS,     oob_size=128),
            TestConfig(raw='random5', page='random5_rs',   page_size=2048,
                       ecc=EccType.RS,     oob_size=128),
            TestConfig(raw='ff',      page='ff_rs',        page_size=2048,
                       ecc=EccType.RS,     oob_size=128),

            # SBL, 2k+64
            TestConfig(raw='zero',    page='zero_sbl',     page_size=2048,
                       ecc=EccType.RS_SBL, oob_size=64),
            TestConfig(raw='random1', page='random1_sbl',  page_size=2048,
                       ecc=EccType.RS_SBL, oob_size=64),
            TestConfig(raw='random2', page='random2_sbl',  page_size=2048,
                       ecc=EccType.RS_SBL, oob_size=64),
            TestConfig(raw='random3', page='random3_sbl',  page_size=2048,
                       ecc=EccType.RS_SBL, oob_size=64),
            TestConfig(raw='random4', page='random4_sbl',  page_size=2048,
                       ecc=EccType.RS_SBL, oob_size=64),
            TestConfig(raw='random5', page='random5_sbl',  page_size=2048,
                       ecc=EccType.RS_SBL, oob_size=64),
            TestConfig(raw='ff',      page='ff_sbl',       page_size=2048,
                       ecc=EccType.RS_SBL, oob_size=64),

            # SBL, 2k+128
            TestConfig(raw='zero',    page='zero_sbl',     page_size=2048,
                       ecc=EccType.RS_SBL, oob_size=128),
            TestConfig(raw='random1', page='random1_sbl',  page_size=2048,
                       ecc=EccType.RS_SBL, oob_size=128),
            TestConfig(raw='random2', page='random2_sbl',  page_size=2048,
                       ecc=EccType.RS_SBL, oob_size=128),
            TestConfig(raw='random3', page='random3_sbl',  page_size=2048,
                       ecc=EccType.RS_SBL, oob_size=128),
            TestConfig(raw='random4', page='random4_sbl',  page_size=2048,
                       ecc=EccType.RS_SBL, oob_size=128),
            TestConfig(raw='random5', page='random5_sbl',  page_size=2048,
                       ecc=EccType.RS_SBL, oob_size=128),
            TestConfig(raw='ff',      page='ff_sbl',       page_size=2048,
                       ecc=EccType.RS_SBL, oob_size=128),

            # BCH4, 2k+64
            TestConfig(raw='zero',    page='zero_bch4',    page_size=2048,
                       ecc=EccType.BCH4,   oob_size=64),
            TestConfig(raw='random1', page='random1_bch4', page_size=2048,
                       ecc=EccType.BCH4,   oob_size=64),
            TestConfig(raw='random2', page='random2_bch4', page_size=2048,
                       ecc=EccType.BCH4,   oob_size=64),
            TestConfig(raw='random3', page='random3_bch4', page_size=2048,
                       ecc=EccType.BCH4,   oob_size=64),
            TestConfig(raw='random4', page='random4_bch4', page_size=2048,
                       ecc=EccType.BCH4,   oob_size=64),
            TestConfig(raw='random5', page='random5_bch4', page_size=2048,
                       ecc=EccType.BCH4,   oob_size=64),
            TestConfig(raw='ff',      page='ff_bch4',      page_size=2048,
                       ecc=EccType.BCH4,   oob_size=64),

            # BCH4, 2k+128
            TestConfig(raw='zero',    page='zero_bch4',    page_size=2048,
                       ecc=EccType.BCH4,   oob_size=128),
            TestConfig(raw='random1', page='random1_bch4', page_size=2048,
                       ecc=EccType.BCH4,   oob_size=128),
            TestConfig(raw='random2', page='random2_bch4', page_size=2048,
                       ecc=EccType.BCH4,   oob_size=128),
            TestConfig(raw='random3', page='random3_bch4', page_size=2048,
                       ecc=EccType.BCH4,   oob_size=128),
            TestConfig(raw='random4', page='random4_bch4', page_size=2048,
                       ecc=EccType.BCH4,   oob_size=128),
            TestConfig(raw='random5', page='random5_bch4', page_size=2048,
                       ecc=EccType.BCH4,   oob_size=128),
            TestConfig(raw='ff',      page='ff_bch4',      page_size=2048,
                       ecc=EccType.BCH4,   oob_size=128),

            # BCH8, 2k+128
            TestConfig(raw='zero',    page='zero_bch8',    page_size=2048,
                       ecc=EccType.BCH8,   oob_size=128),
            TestConfig(raw='random1', page='random1_bch8', page_size=2048,
                       ecc=EccType.BCH8,   oob_size=128),
            TestConfig(raw='random2', page='random2_bch8', page_size=2048,
                       ecc=EccType.BCH8,   oob_size=128),
            TestConfig(raw='random3', page='random3_bch8', page_size=2048,
                       ecc=EccType.BCH8,   oob_size=128),
            TestConfig(raw='random4', page='random4_bch8', page_size=2048,
                       ecc=EccType.BCH8,   oob_size=128),
            TestConfig(raw='random5', page='random5_bch8', page_size=2048,
                       ecc=EccType.BCH8,   oob_size=128),
            TestConfig(raw='ff',      page='ff_bch8',      page_size=2048,
                       ecc=EccType.BCH8,   oob_size=128),

            # RS, 4k+128
            TestConfig(raw='zero',    page='zero_rs',      page_size=4096,
                       ecc=EccType.RS,     oob_size=128),
            TestConfig(raw='random1', page='random1_rs',   page_size=4096,
                       ecc=EccType.RS,     oob_size=128),
            TestConfig(raw='random2', page='random2_rs',   page_size=4096,
                       ecc=EccType.RS,     oob_size=128),
            TestConfig(raw='random3', page='random3_rs',   page_size=4096,
                       ecc=EccType.RS,     oob_size=128),
            TestConfig(raw='random4', page='random4_rs',   page_size=4096,
                       ecc=EccType.RS,     oob_size=128),
            TestConfig(raw='random5', page='random5_rs',   page_size=4096,
                       ecc=EccType.RS,     oob_size=128),
            TestConfig(raw='ff',      page='ff_rs',        page_size=4096,
                       ecc=EccType.RS,     oob_size=128),

            # RS, 4k+256
            TestConfig(raw='zero',    page='zero_rs',      page_size=4096,
                       ecc=EccType.RS,     oob_size=256),
            TestConfig(raw='random1', page='random1_rs',   page_size=4096,
                       ecc=EccType.RS,     oob_size=256),
            TestConfig(raw='random2', page='random2_rs',   page_size=4096,
                       ecc=EccType.RS,     oob_size=256),
            TestConfig(raw='random3', page='random3_rs',   page_size=4096,
                       ecc=EccType.RS,     oob_size=256),
            TestConfig(raw='random4', page='random4_rs',   page_size=4096,
                       ecc=EccType.RS,     oob_size=256),
            TestConfig(raw='random5', page='random5_rs',   page_size=4096,
                       ecc=EccType.RS,     oob_size=256),
            TestConfig(raw='ff',      page='ff_rs',        page_size=4096,
                       ecc=EccType.RS,     oob_size=256),

            # BCH4, 4k+128
            TestConfig(raw='zero',    page='zero_bch4',    page_size=4096,
                       ecc=EccType.BCH4,   oob_size=128),
            TestConfig(raw='random1', page='random1_bch4', page_size=4096,
                       ecc=EccType.BCH4,   oob_size=128),
            TestConfig(raw='random2', page='random2_bch4', page_size=4096,
                       ecc=EccType.BCH4,   oob_size=128),
            TestConfig(raw='random3', page='random3_bch4', page_size=4096,
                       ecc=EccType.BCH4,   oob_size=128),
            TestConfig(raw='random4', page='random4_bch4', page_size=4096,
                       ecc=EccType.BCH4,   oob_size=128),
            TestConfig(raw='random5', page='random5_bch4', page_size=4096,
                       ecc=EccType.BCH4,   oob_size=128),
            TestConfig(raw='ff',      page='ff_bch4',      page_size=4096,
                       ecc=EccType.BCH4,   oob_size=128),

            # BCH4, 4k+256
            TestConfig(raw='zero',    page='zero_bch4',    page_size=4096,
                       ecc=EccType.BCH4,   oob_size=256),
            TestConfig(raw='random1', page='random1_bch4', page_size=4096,
                       ecc=EccType.BCH4,   oob_size=256),
            TestConfig(raw='random2', page='random2_bch4', page_size=4096,
                       ecc=EccType.BCH4,   oob_size=256),
            TestConfig(raw='random3', page='random3_bch4', page_size=4096,
                       ecc=EccType.BCH4,   oob_size=256),
            TestConfig(raw='random4', page='random4_bch4', page_size=4096,
                       ecc=EccType.BCH4,   oob_size=256),
            TestConfig(raw='random5', page='random5_bch4', page_size=4096,
                       ecc=EccType.BCH4,   oob_size=256),
            TestConfig(raw='ff',      page='ff_bch4',      page_size=4096,
                       ecc=EccType.BCH4,   oob_size=256),

            # BCH8, 4k+256
            TestConfig(raw='zero',    page='zero_bch8',    page_size=4096,
                       ecc=EccType.BCH8,   oob_size=256),
            TestConfig(raw='random1', page='random1_bch8', page_size=4096,
                       ecc=EccType.BCH8,   oob_size=256),
            TestConfig(raw='random2', page='random2_bch8', page_size=4096,
                       ecc=EccType.BCH8,   oob_size=256),
            TestConfig(raw='random3', page='random3_bch8', page_size=4096,
                       ecc=EccType.BCH8,   oob_size=256),
            TestConfig(raw='random4', page='random4_bch8', page_size=4096,
                       ecc=EccType.BCH8,   oob_size=256),
            TestConfig(raw='random5', page='random5_bch8', page_size=4096,
                       ecc=EccType.BCH8,   oob_size=256),
            TestConfig(raw='ff',      page='ff_bch8',      page_size=4096,
                       ecc=EccType.BCH8,   oob_size=256),
        ]

        for config in configs:
            with self.subTest(f'Testing {config}'):
                fname = f'in-{config.page_size}-{config.raw}.bin'
                with open(f'tests/resources/{fname}', 'rb') as in_file:
                    input_data = in_file.read()

                fname = f'out-{config.page_size}-{config.page}-{config.oob_size}oob.bin'
                with open(f'tests/resources/{fname}', 'rb') as out_file:
                    output_data = out_file.read()

                page = Page(page_size=config.page_size, oob_size=config.oob_size,
                            widebus=config.widebus, ecc=config.ecc)
                page.program(input_data)

                self.assertEqual(page.data, output_data)

    def test_page_raise(self):
        configs = [
            TestConfig(raw='', page='',
                       page_size=2048, ecc=EccType.RS_SBL,   oob_size=32),
            TestConfig(raw='', page='',
                       page_size=2048, ecc=EccType.RS,   oob_size=32),
            TestConfig(raw='', page='',
                       page_size=2048, ecc=EccType.BCH4,   oob_size=32),
            TestConfig(raw='', page='',
                       page_size=2048, ecc=EccType.BCH8,   oob_size=64),
            TestConfig(raw='', page='',
                       page_size=4096, ecc=EccType.RS,     oob_size=64),
            TestConfig(raw='', page='',
                       page_size=4096, ecc=EccType.BCH4,   oob_size=64),
            TestConfig(raw='', page='',
                       page_size=4096, ecc=EccType.BCH8,   oob_size=128),
        ]

        for config in configs:
            self.assertRaises(ValueError, Page, config.page_size,
                              config.oob_size, config.widebus, config.ecc)

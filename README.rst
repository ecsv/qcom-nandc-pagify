.. SPDX-License-Identifier: MIT
.. SPDX-FileCopyrightText: Sven Eckelmann <sven@narfation.org>

=================
qcom-nandc-pagify
=================

About
=====

The Qualcomm NAND controller takes care of writing and reading pages from
the actual NAND flash chip. It uses a non-standard page layout which splits
the data in smaller partitons and saves these as chunks with ECC, bad block
markers and padding over the data+oob area of the nand pages.

The qcom-nandc-pagify can help to convert a raw image (e.g. Linux, rootfs, ...)
in the page format which is used by the NAND controller. This can then be used
with a NAND flash programmer to initialize the NAND flash chip.

Known NAND controllers which should work the same way are:

* qcom,ipq806x-nand
* qcom,ipq4019-nand
* qcom,ipq6018-nand (tested)
* qcom,ipq8074-nand (tested)
* qcom,sdx55-nand


Usage
=====

Build
-----

The package is PEP517 compatible and can be build using python3-build::

  python3 -m build

The generated wheel  then be installed via pip::

  dist/qcom_nandc_pagify-*-py3-none-any.whl

But the build is not necessary when all dependencies are already installed
on the system. Then it is possible to directly run in from the source
directory::

  python3 -m qcom_nandc_pagify

Unittest
--------

There are a couple of testcases in ``tests/resources``. The ``in-*`` files
are converted to the ``out-*`` files with various parameters. These should
reflect common scenarios. The complete unittest can be run via::

  python3 -m unittest

Installation
------------

It can be installed using pip
`from PyPI <https://pypi.org/project/qcom-nandc-pagify/>`_::

  python3 -m pip install --upgrade qcom-nandc-pagify

Or from the the own build wheel (see avove)::

  python3 -m pip install --upgrade dist/qcom_nandc_pagify-*-py3-none-any.whl

Converting an image
-------------------

The arguments are explained as part of the usage help output::

  qcom_nandc_pagify -h

It is necessary specify an input file and the output file + a couple of
flash dependent parameters::

  # NAND device with 2048+128 large pages with BCH4 (e.g. for Cypress), 8x bus
  qcom-nandc-pagify --infile $INPUT --outfile $OUTPUT --pagesize 2048 --oobsize 128 --ecc bch4

  # NAND device with 2048+64 large pages with RS (e.g. for IPQ806x), 8x bus
  qcom-nandc-pagify --infile $INPUT --outfile $OUTPUT --pagesize 2048 --oobsize 64 --ecc rs

  # NAND device with 2048+64 large pages with RS_SBL (e.g. for IPQ806x, SBL partition), 8x bus
  qcom-nandc-pagify --infile $INPUT --outfile $OUTPUT --pagesize 2048 --oobsize 64 --ecc rs_sbl

  # NAND device with 4096+256 large pages with BCH8 (e.g. Cypress/Hawkeye), 8x bus
  qcom-nandc-pagify --infile $INPUT --outfile $OUTPUT --pagesize 4096 --oobsize 128 --ecc bch8


Physical layout
===============

Page Layout
-----------

The data which should be saved in a page is split into 516 byte portions. Only
the last portion is smaller - 510 bytes of 2048 byte large pages and 484 bytes
for 4096 byte pages. But even the last portion is saved like it would have
been 516 bytes long. The remaining bytes are simply filled with 0xff.

Each data portion is saved with additional data as chunk in the NAND page.

Usually, there are more bytes in the page then chunks. For example,
a 2048 bytes page with 128 bytes OOB will be split like this for 4-bit BCH ECC:

* 516 bytes => 528 bytes for chunk in NAND
* 516 bytes => 528 bytes for chunk in NAND
* 516 bytes => 528 bytes for chunk in NAND
* 510 bytes => 528 bytes for chunk in NAND

This would leave 64 bytes of the 2176 bytes (2048 + 128) uninitialized. But
the remaining bytes in the page can simply filled up with 0xff to make sure
that the page has the correct size in the converted image.

More information about the page layout can be found in Linux's
``qcom_qcom_nandc.c`` under ``qcom_nand_ooblayout_ecc()``

Chunk layout
------------

A chunk is a complex structure with

* first data part
* bad block marker (1 byte on 8x wide bus, 2 byte on 16x wide bus)
* second data part (+padding)
* ECC data
* padding

The first data part and second data part are simply split by a BBM which is
added to each chunk - even when it is not used at all. The position of this
BBM is chosen so that the BBM in the last chunk is at the beginning of the
OOB region of the flash. This means as size for the first data part:

* 2048 bytes page, 528 byte chunk: 464
* 2048 bytes page, 532 byte chunk: 452
* 4096 bytes page, 528 byte chunk: 400
* 4096 bytes page, 532 byte chunk: 372

The size of the ECC data depends on the used algorithm. Following are known

* 4-Bit BCH,  8x bus:  7 bytes ECC
* 4-Bit BCH, 16x bus:  8 bytes ECC
* 8-Bit BCH,  8x bus: 13 bytes ECC
* 8-Bit BCH, 16x bus: 14 bytes ECC
* RS:                 10 bytes ECC

The chunk is then filled up with 0xff to make sure that it has a predefined
size. These size itself depends on the ECC algorithm:

* 4-Bit BCH: 528 byte chunk
* 8-Bit BCH: 532 byte chunk
* RS:        528 byte chunk

More information about the chunk layout can be found in Linux's
``qcom_qcom_nandc.c`` under ``qcom_nandc_read_cw_raw()``.

IPQ806x SBL pages
-----------------

The pages for the secondary bootloader on the IPQ806x didn't had a data
size of 516 bytes per chunk. Instead the data was written in 512 byte chunks
with Reed-Solomon ECC. A chunk will use 532 bytes (1 byte BBM, 10 bytes ECC, 5
bytes padding). The rest of the rules from above still apply.

ECC
===

BCH
---

The polynomial used for calculating the data is 8219 or::

  x**13 + x**4 + x**3 + x**1 + 1

RS
--

The used polynomial for GF(2**10) is 1033 or::

  x ** 10 + x ** 3 + 1

The generator (first consecutive root) is::

  [1, 510, 51, 323, 663, 928, 58, 587, 836]

The data itself is encoded with ``(1015 - chunk_data_size)`` 0 bytes at the
beginning. The resulting 8 10 bit values are reversed, concatenated to a
single 80 bits string and split again into 8 bits portions for storage on the
NAND.

Remarks
=======

There is currently no official documentation from QCA regarding the NAND
controller. Only available devices could be used to analyze the NAND content.
Following features could not yet be tested:

* Reed Solomon ECC on modern devices
* 4K pages
* wide bus mode

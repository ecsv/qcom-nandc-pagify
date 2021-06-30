# SPDX-License-Identifier: MIT
# SPDX-FileCopyrightText: Sven Eckelmann <sven@narfation.org>

import argparse
from typing import List
from . import Page
from . import EccType


def ecc_type(astring: str) -> EccType:
    if astring == 'rs':
        return EccType.RS

    if astring == 'rs_sbl':
        return EccType.RS_SBL

    if astring == 'bch4':
        return EccType.BCH4

    if astring == 'bch8':
        return EccType.BCH8

    raise argparse.ArgumentTypeError('Unknown type %s' % astring)


def positive_int_type(intstr: str) -> int:
    intval = int(intstr)

    if intval <= 0:
        raise argparse.ArgumentTypeError("Must be larger than 0")

    return intval


def parser() -> argparse.ArgumentParser:
    parser_def = argparse.ArgumentParser()

    parser_def.add_argument('--infile', type=argparse.FileType('rb'),
                            required=True, help='Raw image file')
    parser_def.add_argument('--outfile', type=argparse.FileType('wb'),
                            required=True,
                            help='Output file for image in qcom,nandc page format')
    parser_def.add_argument('--pagesize', type=positive_int_type, default=2048,
                            help='Page size of NAND (without OOB) (default: 2048)')
    parser_def.add_argument('--oobsize', type=positive_int_type, default=64,
                            help='Number of OOB bytes per page (default: 64)')
    parser_def.add_argument('--ecc', type=ecc_type, default=EccType.BCH4,
                            help='ECC method used for each chunk [bch4, bch8, rs, rs_sbl] '
                                 '(default: bch4)')
    parser_def.add_argument('--widebus', action='store_true',
                            default=False,
                            help='Enable 16x wide bus support')
    return parser_def


def main(args: List[str] = None) -> None:

    main_parser = parser()
    parsed_args = main_parser.parse_args(args)

    data_in = parsed_args.infile
    data_out = parsed_args.outfile

    page = Page(page_size=parsed_args.pagesize, oob_size=parsed_args.oobsize,
                widebus=parsed_args.widebus, ecc=parsed_args.ecc)

    # process input as "page_size" byte pages (+ necessary padding) and write
    # it to as "page_size + oob_size" pages
    while data_in:
        data = data_in.read(parsed_args.pagesize)
        if len(data) == 0:
            break

        page.program(data)
        data_out.write(page.data)

# SPDX-License-Identifier: MIT
# SPDX-FileCopyrightText: Sven Eckelmann <sven@narfation.org>

import argparse
import sys
from . import Page
from . import ECC_Type
from typing import List


def ecc_type(astring):
    if astring == 'rs':
        return ECC_Type.RS
    elif astring == 'rs_sbl':
        return ECC_Type.RS_SBL
    elif astring == 'bch4':
        return ECC_Type.BCH4
    elif astring == 'bch8':
        return ECC_Type.BCH8
    else:
        raise argparse.ArgumentTypeError(f'Unknown type {astring}')


def positive_int_type(x):
    x = int(x)
    if x <= 0:
        raise argparse.ArgumentTypeError("Must be larger than 0")
    return x

def parser():
    parser = argparse.ArgumentParser()

    parser.add_argument('--infile', type=argparse.FileType('rb'),
                        required=True, help='Raw image file')
    parser.add_argument('--outfile', type=argparse.FileType('wb'),
                        required=True,
                        help='Output file for image in qcom,nandc page format')
    parser.add_argument('--pagesize', type=positive_int_type, default=2048,
                        help='Page size of NAND (without OOB) (default: 2048)')
    parser.add_argument('--oobsize', type=positive_int_type, default=64,
                        help='Number of OOB bytes per page (default: 64)')
    parser.add_argument('--ecc', type=ecc_type, default=ECC_Type.BCH4,
                        help='ECC method used for each chunk [bch4, bch8, rs, rs_sbl] (default: bch4)')
    parser.add_argument('--widebus', action='store_true',
                        default=False,
                        help='Enable 16x wide bus support')
    return parser


def main(args: List[str] = None):

    main_parser = parser()
    parsed_args = main_parser.parse_args(args)

    data_in = parsed_args.infile
    data_out = parsed_args.outfile

    p = Page(page_size=parsed_args.pagesize, oob_size=parsed_args.oobsize,
             widebus=parsed_args.widebus, ecc=parsed_args.ecc)

    # process input as "page_size" byte pages (+ necessary padding) and write
    # it to as "page_size + oob_size" pages
    while data_in:
        data = data_in.read(parsed_args.pagesize)
        if len(data) == 0:
            break

        p.program(data)
        data_out.write(p.data)

"""
Juxtapy

Folder and File juxtaposing in Python

"""

import os
import sys
import argparse

sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from juxtapy import __version__
from juxtapy.juxta import Juxta

def parse_args(args):
    """command line argument parser"""

    parser = argparse.ArgumentParser(
        formatter_class=lambda prog: argparse.RawDescriptionHelpFormatter(prog, max_help_position=30),
        description=__doc__,
        epilog="happy comparing"
    )

    parser.add_argument(
        "-f", "--from_path",
        metavar="STR",
        help="from (left) directory or file path"
    )
    parser.add_argument(
        "-t", "--to_path",
        metavar="STR",
        help="to (right) directory or file path"
    )
    parser.add_argument(
        "-o", "--output_path",
        metavar="STR",
        help="output path"
    )
    parser.add_argument(
        "--file_filter",
        metavar="STR",
        default="*.pyc",
        help="fnmatch file filter string (default: '*.pyc')"
    )
    parser.add_argument(
        "--file_ignore",
        metavar="STR",
        default=".DS_Store,.localized",
        help="comma separated files to ignore (default: '.DS_Store,.localized')"
    )
    parser.add_argument(
        "--q", "--quiet",
        action="store_true",
        help="show no info"
    )
    parser.add_argument(
        "--version",
        help="display the program's version",
        action="version",
        version="%(prog)s "+__version__
    )

    return parser.parse_args(args)

def main(lineargs):
    """command line program"""

    # process arguments
    args = parse_args(lineargs)
    args.file_ignore = args.file_ignore.split(',')

    # do comparison
    jxt = Juxta(args.from_path, args.to_path, args.output_path, args.file_filter, args.file_ignore, args.quiet)
    response = jxt.compare()
    print response

if __name__ == "__main__":
    main(sys.argv[1:])

"""
Juxtapy
Folder and File Comparison

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
        epilog="by tmthydvnprt"
    )
    
    parser.add_argument(
        "-f", "--from",
        metavar="STR",
        help="from (left) directory or file path"
    )
    parser.add_argument(
        "-t", "--to",
        metavar="STR",
        help="to (right) directory or file path"        
    )
    parser.add_argument(
        "-o", "--output",
        metavar="STR",
        help="output path"        
    )
    parser.add_argument(
        "--filter",
        metavar="STR",
        default="*.pyc",
        help="fnmatch file filter string (default: '*.pyc')"
    )
    parser.add_argument(
        "--ignore",
        metavar="STR",
        default=".DS_Store,.localized",
        help="comma separated files to ignore (default: '.DS_Store,.localized')"
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
    args.ignore = args.ignore.split(',')

    # do comparison    
    jxt = Juxta(args.from, args.to, args.output, args.filter, args.ignore)
    print jxt.compare()    
    
if __name__ == "__main__":
    main(sys.argv[1:])

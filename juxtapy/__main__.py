"""
    Executable version of project package
"""

import os
import sys
import argparse

def parse_args(args):
    """command line argument parser"""
    
    # ...
    
    # return parser.parse_args(args)

def main(lineargs):
    """command line program"""

    # process arguments
    args = parse_args(lineargs)

    # do something
    
if __name__ == "__main__":
    main(sys.argv[1:])

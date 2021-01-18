#!/usr/bin/python3
import argparse
import os.path
import re
from matchgrowth import *

def valid_file(inputfile):
    if not os.path.isfile(inputfile):
        raise argparse.ArgumentTypeError('mysql dump file does not exist')
    return inputfile

arg_parser = argparse.ArgumentParser(description='Tool for estimating growth rates')
arg_parser.add_argument('--file', dest='file', action='store', required=True, type=valid_file, help='CSV input file with measurements')
arg_parser.add_argument('--col1', dest='col1', action='store', required=True, help='data column 1 from the CSV')
arg_parser.add_argument('--col2', dest='col2', action='store', required=True, help='data column 2 from the CSV')
args   = arg_parser.parse_args()


run_from_file(args.file,args.col1,args.col2)


#!/usr/bin/python3
import argparse
import os.path
import re
from matchgrowth import *

def valid_file(inputfile):
    if not os.path.isfile(inputfile):
        raise argparse.ArgumentTypeError('CSV input file does not exist')
    return inputfile

arg_parser = argparse.ArgumentParser(description='Tool for estimating growth rates')
arg_parser.add_argument('--infile',   dest='infile'     , action='store', required=True, type=valid_file, help='CSV input file with measurements')
arg_parser.add_argument('--outfile',  dest='outfile'    , action='store', default=None, required=False, help='PNG file to write the plot to')
arg_parser.add_argument('--col1',     dest='col1'       , action='store', required=True, help='data column 1 from the CSV')
arg_parser.add_argument('--col2',     dest='col2'       , action='store', required=True, help='data column 2 from the CSV')
arg_parser.add_argument('--top',      dest='top'        , action='store', default=None, required=False, type=int, help='only print top N closest growth rates')
arg_parser.add_argument('--catalog',  dest='catalog'    , action='store', default='default', help='select the function catalog to use')
arg_parser.add_argument('--debug', action='store_true', default=False, help='enable debug mode')
arg_parser.add_argument('--plot',     dest='plot_type'  , action='store', default='normal', help='plot type (normal|loglog)')
cli_args = arg_parser.parse_args()

if cli_args.debug:
    print(cli_args)

text_to_catalog = {
    'default': common_catalog,
    'unbounded': unbounded_catalog,
}
catalog_obj = text_to_catalog[cli_args.catalog]
run_from_file(cli_args,catalog_obj)


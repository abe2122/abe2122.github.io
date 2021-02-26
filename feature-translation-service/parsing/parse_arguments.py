#!/usr/bin/env python

'''Testing'''

import argparse

def parse_swot_arguments():
    '''Testing'''

    # Parse command line arguments
    parser = argparse.ArgumentParser()
    required = parser.add_argument_group('required arguments')
    required.add_argument('-i', help='input directory', required=True)
    required.add_argument('-o', help='output directory', required=True)
    args = parser.parse_args()
    args = vars(args)

    return args

def parse_huc_arguments():
    '''Testing'''

    # Parse command line arguments
    parser = argparse.ArgumentParser()
    required = parser.add_argument_group('required arguments')
    required.add_argument('-i', help='input directory', required=True)
    required.add_argument('-o', help='output directory', required=True)
    required.add_argument('-v', help='max vertices of polygons', required=True)
    args = parser.parse_args()
    args = vars(args)

    return args

#!/usr/bin/env python

'''Set of primary functions used create the HUC portion of the Feature Translation
   Service. Takes in command line input, and aggregates input USGS data into a
   single, consolidated database of simplified polygons and bounding boxes.'''

import sys
import os

from simplify_huc import create_resolutions_and_combine
from remove_multipolygons import remove


def combine(arguments):
    '''Create final database including simplified polygons and HUCs.'''

    # Read in command line arguments
    in_dir = arguments['i']
    out_dir = arguments['o']
    vertices = arguments['v']

    if not in_dir.endswith("/"):
        in_dir += "/"
    if not out_dir.endswith("/"):
        out_dir += "/"

    huc_list = []
    for root, dirs, files in os.walk(in_dir):
        for file in files:
            if file.endswith(".shp") and file.startswith("WBDHU"):
                huc_list.append(os.path.join(root, file))

    if not huc_list:
        print("No shapefiles found. Make sure you have a directory of HUC subfolders in place.")
        exit()

    # Create local directory at 'output directory' location if it doesn't already
    # exist
    if not os.path.exists(out_dir):
        os.makedirs(out_dir)

    print("\nCreating HUC dataset... ")
    final_df = parse_huc(huc_list)
    final_df['Geo_Without_Multipolygons'] = final_df.apply(lambda row:
                                                           remove(row['Geometry']), axis=1)

    # Function in 'simplify_HUC.py'
    create_resolutions_and_combine(final_df, out_dir, vertices)


if __name__ == "__main__":

    sys.path.insert(0, '../parsing/')
    from parse_arguments import parse_huc_arguments
    from parse_huc import parse_huc

    ARGS = parse_huc_arguments()
    combine(ARGS)

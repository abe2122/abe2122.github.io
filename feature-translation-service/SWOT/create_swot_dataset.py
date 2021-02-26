#!/usr/bin/env python

'''Set of primary functions used create the SWOT portion of the Feature Translation
   Service. Takes in command line input, and builds a consolidated database
   containing mappints between SWOT Feature IDs and geometries.'''

import sys
import os


def combine(args):
    '''Primary function that builds database and writes it to a SWOT_Data.csv
       file.'''

    # Read in command line arguments
    in_dir = args['i']
    out_dir = args['o']

    # Append / if missing from input
    if not in_dir.endswith("/"):
        in_dir += "/"
    if not out_dir.endswith("/"):
        out_dir += "/"

    # Generate list of all shapefiles in input directory
    swot_list = []
    for root, dirs, files in os.walk(in_dir):
        for file in files:
            if file.endswith('.shp'):
                swot_list.append(os.path.join(root, file))

    if not swot_list:
        print("No shapefiles found. Make sure you have a SWOT shapefiles in your input directory.")
        exit()

    # Create local directory at 'output directory' location if it doesn't already
    # exist
    if not os.path.exists(out_dir):
        os.makedirs(out_dir)

    print("\nCreating SWOT dataset...\n")
    final_df = parse_swot(swot_list)

    # Output to .csv to be uploaded to mySQL database.
    final_df.to_csv(out_dir + "SWOT_Data.csv", index=False)
    print("\nDone! You can find the output file under: {}\n".format(out_dir + "SWOT_Data.csv"))


if __name__ == "__main__":

    sys.path.insert(0, '../parsing/')
    from parse_swot import parse_swot
    from parse_arguments import parse_swot_arguments

    ARGS = parse_swot_arguments()
    combine(ARGS)

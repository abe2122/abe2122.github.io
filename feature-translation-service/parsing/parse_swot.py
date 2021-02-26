#!/usr/bin/env python

'''Testing'''

import re

import geopandas as gpd
from tqdm import tqdm
import pandas as pd

def convert(row):
    '''Testing'''

    # Return lat1, lon1 string of point for CMR
    if row['type'] == "Point":
        return "point={},{}".format(row['geometry'].x, row['geometry'].y)

    # Return lat1, lon1, lat2, lon2, (...) string for CMR
    linestring = str(list(row['geometry'].coords))
    linestring = re.sub(r'[()[\]\s+]', '', linestring)

    return "line={}".format(linestring)


def parse_swot(swot_list):
    '''Testing'''

    # Initialize and empty dataframe to store final SWOT database
    final_df = pd.DataFrame()
    for element in tqdm(swot_list):

        # Read in shapefile and convert to Pandas dataframe
        gdf = gpd.read_file(element)
        pdf = pd.DataFrame(gdf)

        # Remove extraneous information from dataframe, leaving the following
        # five categories
        pdf = pdf[['basin_code', 'segID', 'segInd', 'geometry', 'lakeflag']]
        pdf['segInd'] = pdf['segInd'].astype(str)

        # Remove indices that are negative. Maybe a mistake in the SWORD database?
        # Only ~600 / 10,000,000 have this negative.
        pdf.drop(pdf[pdf['segInd'].str.startswith("-")].index, inplace=True)

        # Pad each column with zeros for same length
        # SegID: 1234 -> 1234
        # SegID: 1 -> 0001
        pdf['basin_code'] = pdf['basin_code'].apply(lambda x: str(x).zfill(6))
        pdf['segID'] = pdf['segID'].apply(lambda x: str(x).zfill(4))
        pdf['segInd'] = pdf['segInd'].apply(lambda x: str(x).zfill(5))

        # Create swot Feature ID according to standard concatenation of:
        # continent code + basin code + reach + node + lakeflag
        pdf['SWOT_ID'] = pdf['basin_code'] + pdf['segID'] + pdf['segInd'] + pdf['lakeflag'].map(str)
        pdf['SWOT_ID'] = pdf['SWOT_ID'].astype(str)
        pdf = pdf[['SWOT_ID', 'geometry']]

        # Column of types: either "Point" or "LineString"
        # Used in Lambda function
        pdf['type'] = pdf['geometry'].apply(lambda row: row.type)

        # Convert geometry to CMR queryable string
        gdf = gpd.GeoDataFrame(pdf, geometry='geometry')
        gdf['geometry'] = gdf.apply(lambda row: convert(row), axis=1)

        pdf = pd.DataFrame(gdf)
        pdf.drop(['type'], inplace=True, axis=1)

        # Concatenate each shapefile DataFrame together
        final_df = pd.concat([final_df, pdf])

    return final_df

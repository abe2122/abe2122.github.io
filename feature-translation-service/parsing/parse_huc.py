#!/usr/bin/env python

'''Creates single, consolidated HUC database without simplified polygons.'''

import geopandas as gpd
import pandas as pd

def parse_huc(huc_list):
    '''Creates single, consolidated HUC database without simplified polygons.
       Ready for simplification process next.'''

    final_df = pd.DataFrame()
    for element in huc_list:
        temp_df = gpd.read_file(element)
        # Extract HUC level for indexing (2, 4, 6, 8, ...)
        try:
            huc_category = int(element.split('.')[-2][-2:])
        except ValueError:
            huc_category = int(element.split('.')[-2][-1:])

        temp_df = temp_df[['HUC{}'.format(huc_category), 'Name', 'geometry']]
        temp_df.columns = ['HUC', 'Region', 'Geometry']
        temp_df['HUC'] = temp_df['HUC'].astype(str)

        # Concatenate each shapefile DataFrame together
        final_df = pd.concat([final_df, temp_df])

    return final_df

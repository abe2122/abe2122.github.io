#!/usr/bin/env python

'''Function for removing multipolygons from a geometry - choosing the largest
   area polygon as the response.'''

def remove(geometry):
    '''Simplifies multipolygon. Otherwise returns normal polygon.'''

    if geometry.type == 'MultiPolygon':
        return max(geometry, key=lambda a: a.area)

    return geometry

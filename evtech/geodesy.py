""" Functions for converting coordinates """

import utm
from pyproj import CRS

def utm_crs_from_latlon(lat, lon):
    """ Determines the UTM CRS from a given lat lon point
    
    :param lat: The latitude
    :type lat: float
    :param lon: The longitude
    :type lon: float
    :return: A coordinate system for the associated UTM zone
    :rtype: class:`pyroj.CRS`
    """
    _, _, zone, _ = utm.from_latlon(lat, lon)
    if lat >= 0:
        epsg = '326' + str(zone)
    else:
        epsg = '327' + str(zone)

    return CRS.from_user_input(int(epsg))
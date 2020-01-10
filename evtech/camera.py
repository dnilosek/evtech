"""Camera class for evtech."""

import numpy as np
import utm

from pyproj import CRS

from .geodesy import utm_crs_from_latlon

class Camera():
    """This class represents camera information for a given image and allows for world<->camera interactions
    
    :param proj: The 3x4 projection matrix for the camera
    :type proj: class: `numpy.array`
    :param bounds: The bounds of the image chip within the larger image [x_min, y_min, x_max, y_max]
    :type bounds: list
    :param cen: The center of the camera [x, y, z]
    :type cen: list
    :param geo_bounds: The geographic bounds of the image in lat/lon [x_min, y_min, x_max, y_max]
    :type geo_bounds: list
    :param elev: The average elevation of the image
    :type elev: float
    :param crs: The coordinate system for the projection matrix
    :type crs: class: `pyproj.CRS`
    """

    def __init__(self, proj, bounds, cen, geo_bounds, elev, crs):
        """ Constructor method
        """
        self.projection_matrix = proj
        self.image_bounds = bounds
        self.image_center = cen
        self.geo_bounds = geo_bounds
        self.elevation = elev
        self.crs = crs


def camera_from_json(json_data):
    """ Generate a camera from the seralized JSON data
    
    :param json_data: The json data loaded from the serlized JSON
    :type json_data: dict
    :return: A camera object
    :rtype: classs
    """
    # Determine proper UTM zone
    crs = utm_crs_from_latlon(json_data["geo_bounds"][1], 
                                json_data["geo_bounds"][0])

    return Camera(np.array(json_data["projection"]), json_data["bounds"], 
                    json_data["camera_center"],json_data["geo_bounds"], 
                    json_data["elevation"], crs)
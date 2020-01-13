"""Camera class for evtech."""

import numpy as np
import utm
import cv2

from pyproj import CRS, Transformer

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
    :param image_path: The filepath to the image data
    :type path: str
    """

    def __init__(self, proj, bounds, cen, geo_bounds, elev, crs, image_path):
        """ Constructor method
        """
        self.projection_matrix = proj
        self.image_bounds = bounds
        self.image_center = cen
        self.geo_bounds = geo_bounds
        self.elevation = elev
        self.crs = crs
        self.image_path = image_path

    def set_path(self, image_path):
        """ Mutator to set path data member
        
        :param path: Path to image data
        :type path: string
        """
        self.image_path = image_path

    def project_to_camera(self, lon, lat, elevation):
        """ Project a lat/lon/elevation point into the image
        
        :param lat: The latitiude
        :type lat: float
        :param lon: The longitiude
        :type lon: float
        :param elevation: The elevation
        :type elevation: float
        :return: The row, col value of the pixel
        :rtype: class: `np.Array`
        """

        # Convert lat/lon/elev to camera CRS
        transformer = Transformer.from_crs(CRS.from_user_input(4326),self.crs, always_xy=True)
        x,y,z = transformer.transform(lon, lat, elevation)
        pt = np.transpose(np.array([[x,y,z,1.0]]))

        # Do projection
        img_pt_h = self.projection_matrix @ pt
        img_pt = img_pt_h / img_pt_h[2]

        # Offset pixel by bounds
        img_pt[0] -= self.image_bounds[0]
        img_pt[1] -= self.image_bounds[1]
        img_pt = np.transpose(img_pt)
        return img_pt[0][0:2]
    
    def load_image(self, loader=cv2.imread):
        """ Load the image for this camera
        
        :param loader: A function to load the image, defaults to cv2.imread
        :type loader: function, optional
        :return: image data
        :rtype: numpy.array
        """
        return loader(self.image_path)

def camera_from_json(json_data, image_path = ""):
    """ Generate a camera from the seralized JSON data
    
    :param json_data: The json data loaded from the serlized JSON
    :type json_data: dict
    :param image_path: The path to the associated image data
    :type image_path: str, optional
    :return: A camera object
    :rtype: classs
    """
    # Determine proper UTM zone
    crs = utm_crs_from_latlon(json_data["geo_bounds"][1], 
                                json_data["geo_bounds"][0])

    return Camera(np.array(json_data["projection"]), json_data["bounds"], 
                    json_data["camera_center"],json_data["geo_bounds"], 
                    json_data["elevation"], crs, image_path)
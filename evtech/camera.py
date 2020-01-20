"""Camera class for evtech."""

import numpy as np
import utm
import cv2
import math
import scipy.optimize as optimize

from pyproj import CRS, Transformer
from shapely.geometry import Polygon, box

from .geodesy import utm_crs_from_latlon
from .ray import Ray

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
    :param crs: The coordinate system for the projection matrix (Must be linear such as UTM)
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

    def get_bounds(self):
        """ Get the bounds of the camera
        :return: The bounds of the image on the ground
        :rtype: class: `shapely.Polygon`
        """
        bounds = box(minx = self.geo_bounds[0], miny=self.geo_bounds[1], 
                    maxx = self.geo_bounds[2], maxy=self.geo_bounds[3])
        return(Polygon(bounds))

    def project_from_camera(self, col, row):
        """ Project a ray from the camera

        :param col: The column index of the pixel to project
        :type col: float
        :param row: The row index of the pixel to project
        :type row: float

        :return: A ray from the camera
        :rtype: class: `evtech.Ray`
        """

        # subset the projection matrix
        m = self.projection_matrix[0:3,0:3]

        # Offset for crop
        col, row = self.to_full_image(col,row)

        # Get point and project to to normalized plane
        pt = np.transpose(np.array([[col,row,1.0]]))
        norm_pt = np.linalg.inv(m) @ pt

        # Create ray
        [vec_norm_pt] = np.transpose(norm_pt).tolist()
        return Ray(self.image_center[0:3], vec_norm_pt, self.crs)

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

    def height_between_points(self, base_point, peak_point, elev=None):
        """ Compute the height between two image points, given the elevation of the base point. 
        If no elevation is passed the stored elevation will be used.

        :param base_point: The image point at the given elevation
        :type base_point: list
        :param peak_point: The image point to compute the height at
        :type peak_point: list
        :param elev: The associated elevation of the base point, defaults to None
        :type elev: float, optional
        """
        if not elev:
            elev = self.elevation
        
        # Compute rays from each point
        base_ray = self.project_from_camera(base_point[0],base_point[1])
        peak_ray = self.project_from_camera(peak_point[0],peak_point[1])

        # Compute the cosine of the angle between the two rays
        [base_dir] = np.transpose(base_ray.direction)
        [peak_dir] = np.transpose(peak_ray.direction)

        dt = np.dot(base_dir, peak_dir)
        c = dt/np.linalg.norm(base_dir)/np.linalg.norm(peak_dir)

        # Compute depth at given elevation
        depth = base_ray.depth_at_elevation(elev)

        # Get depth at midpoint between points
        depth_mid = depth*c

        # Extract focal length from proj matrix
        camera_matrix,_,_,_,_,_,_ = cv2.decomposeProjectionMatrix(self.projection_matrix)
        focal_x = camera_matrix[0][0]
        focal_y = camera_matrix[1][1]
        focal = (focal_x + focal_y) / 2

        # Compute height using simlar triangles
        dist = np.linalg.norm(np.array(base_point) - np.array(peak_point))
        height = dist / focal * depth_mid
        return height[0]

    def to_full_image(self, col, row):
        """ Convert an image point from the subset image to the full image
        
        :param col: The column to offset
        :type col: float
        :param row: The row to offset
        :type row: float
        :return: The offset row,col
        :rtype: tuple
        """
        r_col = col + self.image_bounds[0]
        r_row = row + self.image_bounds[1]
        return r_col, r_row
        
    def load_image(self, loader=cv2.imread):
        """ Load the image for this camera
        
        :param loader: A function to load the image, defaults to cv2.imread
        :type loader: function, optional
        :return: image data
        :rtype: numpy.array
        """
        return loader(str(self.image_path))

def camera_from_json(json_data, image_path = ""):
    """ Generate a camera from the seralized JSON data
    
    :param json_data: The json data loaded from the serlized JSON
    :type json_data: dict
    :param image_path: The path to the associated image data
    :type image_path: str, optional
    :return: A camera object
    :rtype: evtech.Camera
    """
    # Determine proper UTM zone
    crs = utm_crs_from_latlon(json_data["geo_bounds"][1], 
                                json_data["geo_bounds"][0])

    return Camera(np.array(json_data["projection"]), json_data["bounds"], 
                    json_data["camera_center"],json_data["geo_bounds"], 
                    json_data["elevation"], crs, image_path)

def triangulate_point_from_cameras(cameras, points, to_latlng = False):
#     """ Triangulates a 3D point from two cameras and two image points
    
#     :param camera_1: The first camera
#     :type camera_1: evtech.Camera
#     :param point_1: The first image point as a 2 element list [col,row]
#     :type point_1: list
#     :param camera_2: The second camera
#     :type camera_2: evtech.Camera
#     :param point_2: The second image point as a 2 element list [col,row]
#     :type point_2: list
#     :param to_latlng: Flag to return the point as lat/lng/elevation, otherwise will return in the camera's CRS
#     :type to_latlng: bool
#     :return: A 3d point
#     :rtype: numpy.Array
#     """

    # Get LS initial guess at point 
    A = []
    for cam, pt in zip(cameras, points):
        x,y = cam.to_full_image(float(pt[0]),float(pt[1]))
        A.append(x * cam.projection_matrix[2,:] - cam.projection_matrix[0,:])
        A.append(y * cam.projection_matrix[2,:] - cam.projection_matrix[1,:])

    # Solve for X
    u,d,vt=np.linalg.svd(A)
    X = vt[-1,0:3]/vt[-1,3] # normalize

    # Optimize by minmizing the reprojection error
    def f(world_pt):
        res_sum = 0
        world_pt_h = np.append(world_pt, [1.0])
        for cam, pt in zip(cameras, points):
            proj = cam.projection_matrix @ world_pt_h
            proj = proj / proj[2]
            x,y = cam.to_full_image(float(pt[0]),float(pt[1]))
            res_x = abs(x - proj[0])
            res_y = abs(y - proj[1])
            # For numerical stability
            res = (res_x*res_x + res_y*res_y)**0.5 * 1000
            res_sum += res
        return res_sum

    X0 = np.transpose([X[0], X[1], X[2]])
    result = optimize.minimize(f, X0, method='nelder-mead')
    X = result.x

    # Convert if needed
    if to_latlng:
        transformer = Transformer.from_crs(cameras[0].crs, CRS.from_user_input(4326), always_xy=True)
        X[0],X[1],X[2] = transformer.transform(X[0], X[1], X[2])

    return X

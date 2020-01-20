=====
Usage
=====

To use EVTech in a project::

    import evtech

In order to load a dataset (a single collection of images)::

    # Load the cameras
    nadirs, obliques = evtech.load_dataset('/path/to/dataset')

    # Get the image data for the first nadir camera as a numpy array
    nadir_cam = nadirs[0]
    img = nadir_cam.load_image()

The camera object also stores the average elevation of the image and the geographical bounds of the image, which can be retreived as a Shapely polgon::

    # Get average elevation for image
    elev = nadir_cam.elevation

    # Get bounding polygon
    bounds = nadir_cam.get_bounds()

    # Create geojson from bounds using shapely, json 
    from shapely.geometry import mapping
    import json

    geo_json = json.dumps(mapping(bounds))

From here you can also look at operations with the camera, such as projecting a ray from the camera at a given pixel. Also projecting a latitude, longitude, elevation point into the camera to get the pixel location::

    image_pt = nadir_cam.project_to_camera(lon, lat, elevation)
    ray = nadir_cam.project_from_camera(col, row)

Rays can be used with ground elevation to find the intersection of the pixel and the ground::

    ground_point_at_pxiel = ray.intersect_at_elevation(nadir_cam.elevation)

We have provided a simple single-image height measurement function that uses the camera and two points to compute the height of an object at a given elevation::

    height = nadir_cam.height_between_points(base_img_pt, peak_image_pt, nadir_cam.elevation)

Lastly, we have proivded a function to take multiple cameras and associated image points, and triangulate a three dimensional point::

    # Load cameras from dataset
    cam1 = nadirs[0]
    cam2 = obliques[1]
    cam3 = obliques[2]
    cams = [cam1, cam2, cam3]

    # Points from images associated with cam1, cam2, cam3
    pt1 = [605,171]
    pt2 = [304,536]
    pt3 = [879,441]
    pts = [pt1, pt2, pt3]

    world_pt = evtech.triangulate_point_from_cameras(cams, pts)

OpenCV has a number of tools that can be used for image manipulation and display, refer to the `imgproc <https://docs.opencv.org/4.2.0/d7/dbd/group__imgproc.html>`_ and `highgui <https://docs.opencv.org/4.2.0/d7/dfc/group__highgui.html>`_ packages. Note that these are c++ bindings, you can find many examples that may be helpful on how to use the OpenCV Python bindings `here <https://docs.opencv.org/4.2.0/d6/d00/tutorial_py_root.html>`_::

    import cv2

    # Get image
    img = nadir_cam.load_image()

    # Display an image
    cv2.namedWindow('image', cv2.WINDOW_NORMAL)
    cv2.imshow('image',img)
    k = cv2.waitKey(0)

    # wait for ESC key to exit
    if k == 27:
        cv2.destroyAllWindows()
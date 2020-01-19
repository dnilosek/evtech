=====
Usage
=====

To use EVTech in a project::

    import evtech

In order to load a dataset (a single collection of images)::

    # Load the cameras
    nadirs, obliques = evtech.load_dataset('/path/to/dataset')

    # Get the image data for the first nadir camera as a numpy array
    img = nadirs[0].load_image()

From where you can also look at operations with the camera, such as projecting a ray from the camera at a given pixel. Also projecting a latitude, longitude, elevation point into the camera to get the pixel location::

    # Fill in 

The camera object also stores the average elevation of the image and the geographical bounds of the image, which can be retreived as a Shapely polgon::

    # Fill in

We have provided a simple single-image height measurement function that uses the camera and two points to compute the height of an object::

    # Fill in

Lastly, we have proivded a function to take multiple cameras and associated image points, and triangulate a three dimensional point::

    # Fill in

OpenCV has a number of tools that can be used for image manipulation and display, refer to the `imgproc <https://docs.opencv.org/4.2.0/d7/dbd/group__imgproc.html>`_ and `highgui <https://docs.opencv.org/4.2.0/d7/dfc/group__highgui.html>`_ packages. Note that these are c++ bindings, you can find many examples that may be helpful on how to use the OpenCV Python bindings `here <https://docs.opencv.org/4.2.0/d6/d00/tutorial_py_root.html>`_::

    # Fill in
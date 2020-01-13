=====
Usage
=====

To use EVTech in a project::

    import evtech

In order to load a dataset (a single collection of images)

    # Load the cameras
    nadirs, obliques = evtech.load_dataset('/path/to/dataset')

    # Get the image data for the first nadir camera as a numpy array
    img = nadirs[0].load_image()
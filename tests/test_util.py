def rmtree(root):
    """ Function to remove a directory and its contents
    
    :param root: The root directory
    :type root: pathlib.Path
    """
    for p in root.iterdir():
        if p.is_dir():
            rmtree(p)
        else:
            p.unlink()

    root.rmdir()
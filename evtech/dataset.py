from pathlib import Path


def load_dataset(dir_path):
    """ Loads a dataset into two arrays of cameras
    
    :param dir_path: Path to the dataset
    :type dir_path: string
    """
    nadir_path = Path(dir_path).joinpath("nadirs")
    oblique_path = Path(dir_path).joinpath("obliques")

    print(nadir_path, oblique_path)


from pathlib import Path

from evtech import camera_from_json

def load_dataset(dir_path, loader = camera_from_json):
    """ Loads a dataset into two arrays of cameras
    
    :param dir_path: Path to the dataset
    :type dir_path: string
    :param loader: Callable function to load a single image/metadata pair
    :param loader: function(str, str), optional
    """
    nadir_path = Path(dir_path).joinpath("nadirs")
    oblique_path = Path(dir_path).joinpath("obliques")

    # Find Jpg/Json pairs
    nadirs = []
    for img in nadir_path.glob('*.jpg'):
        img_data = img.with_suffix('').with_suffix(".json")
        print(img_data)
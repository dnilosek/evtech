import json

from pathlib import Path
from evtech import camera_from_json

def load_dataset(dir_path, loader = camera_from_json):
    """ Loads a dataset into two arrays of cameras
    
    :param dir_path: Path to the dataset
    :type dir_path: string
    :param loader: Callable function to load a single image/metadata pair
    :param loader: function(str, str), optional
    :return: A tuple with list of nadir cams and list of oblique cams
    :rtype: tuple: list,list
    """
    nadir_path = Path(dir_path).joinpath("nadirs")
    oblique_path = Path(dir_path).joinpath("obliques")

    # Find Jpg/Json pairs
    def load(path):
        cams = []
        for img in path.glob('*.jpg'):
            img_data_path = img.with_suffix('').with_suffix(".json")

            # Load json data
            with open(img_data_path) as f:
                img_data = json.load(f)

            # Add camera
            cams.append(loader(img_data,img))
        return cams

    nadirs = load(nadir_path)
    obliques = load(oblique_path)

    return nadirs, obliques

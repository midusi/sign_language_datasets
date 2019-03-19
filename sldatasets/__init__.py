__version__ = "0.0.1"

from sldatasets.lsa64 import LSA64
import os
from pathlib import Path


# association between datasets_ids and loader classes
datasets = {"lsa64": LSA64
            # "boston":boston
            }


def get(dataset_id, datasets_path=None, **kwargs):

    # if datasets_path was not specified, use default
    if datasets_path == None:
        datasets_path = os.path.join(Path.home(), '.lsdatasets')
    os.makedirs(datasets_path, exist_ok=True)

    if dataset_id in datasets:
        dataset_loader_class = datasets[dataset_id]
        dataset_loader = dataset_loader_class(**kwargs)
        return dataset_loader.load_data(datasets_path)
    else:
        raise ValueError(
            f"Unknown dataset {dataset_id}. Valid options are {','.join(datasets.keys())}")


def positions_from(dataset, version):
    import datasethandler as dh
    return dh.DatasetHandler(version).get_humans_from_dataset(dataset)

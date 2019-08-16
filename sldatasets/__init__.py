__version__ = "0.0.1"

from sldatasets.Datasetloader import LSA64, ASLLVD
from sldatasets.video_dataset import Videodataset
import os
from pathlib import Path


# association between datasets_ids and loader classes
datasets = {"lsa64": LSA64,
            "asllvd": ASLLVD
            }


def get(dataset_id, **kwargs):
    return Videodataset(dataset_id, **kwargs)


def load_anotations(dataset_id="lsa64", **kwargs):
    loader = get_loader(dataset_id, kwargs.get('version'), kwargs.get('path'))
    return loader.load_annotations()


def get_loader(dataset_id, version, dataset_path):
    if dataset_id in datasets:
        return datasets[dataset_id](version, dataset_path)
    else:
        raise ValueError(
            f"Unknown dataset {dataset_id}. Valid options are {','.join(datasets.keys())}")

__version__ = "0.0.1"

from sldatasets.lsa64 import LSA64
import os
from pathlib import Path


# association between datasets_ids and loader classes
datasets = {"lsa64": LSA64
            # "boston":boston
            }


def get(dataset_id, **kwargs):
    loader = get_loader(dataset_id, kwargs.get('version'), kwargs.get('path'))
    return loader.load_data(kwargs.get('index'))


def positions_from(dataset, version):
    from sldatasets.datasethandler import DatasetHandler as dh
    return dh(version).get_humans_from_dataset(dataset)


def load_anotations(dataset_id="lsa64", **kwargs):
    loader = get_loader(dataset_id, kwargs.get('version'), kwargs.get('path'))
    return loader.load_anotations()


def get_loader(dataset_id, version, dataset_path):
    if dataset_id in datasets:
        return datasets[dataset_id](version, dataset_path)
    else:
        raise ValueError(
            f"Unknown dataset {dataset_id}. Valid options are {','.join(datasets.keys())}")

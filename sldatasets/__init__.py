__version__ = "0.0.1"

from sldatasets.Datasetloader import LSA64, Boston
import os
from pathlib import Path


# association between datasets_ids and loader classes
datasets = {"lsa64": LSA64,
            "boston": Boston
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


def walk_through_pre(video_tuple):
    import numpy as np
    import sldatasets as sld
    npzfile = np.load(sld.load_anotations(version='pre'))
    x = video_tuple[1].split('_')
    index = (int(x[0])-1)*50+(int(x[1])-1)*5+int(x[2])-1
    video = video_tuple[0]
    n, _h, _w, _c = video.shape
    frames = []
    for j in range(0, n):
        frames.append(get_tuple(video[j, :], j, index, npzfile))
    return (n for n in frames)


def get_tuple(frame, j, index, npz):
    tup = (frame,)
    for key in npz.files:
        anotation = npz[key][index]
        if key.split('_').__contains__('exist'):
            tup = tup + (anotation[j],)
        elif key.split('_').__contains__('positions'):
            tup = tup + (anotation[0][j],
                         anotation[1][j])
        else:
            tup = tup + (anotation[0],)
    return tup

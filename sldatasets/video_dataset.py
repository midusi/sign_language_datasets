from collections.abc import Generator
from sldatasets.Datasetloader import LSA64, Boston
datasets = {"lsa64": LSA64,
            "boston": Boston
            }


class Videodataset(Generator):

    def __init__(self, dataset_id, **kwargs):
        self.loader = self.get_loader(dataset_id, kwargs.get(
            'version'), kwargs.get('path'))
        self.data = self.loader.load_data(**kwargs)

    def send(self, ignored_arg):
        try:
            return self.data.__next__()
        except:
            self.throw()

    def throw(self, type=None, value=None, traceback=None):
        raise StopIteration

    def get_loader(self, dataset_id, version, dataset_path):
        if dataset_id in datasets:
            return datasets[dataset_id](version, dataset_path)
        else:
            raise ValueError(
                f"Unknown dataset {dataset_id}. Valid options are {','.join(datasets.keys())}")

    def summary(self):
        print(self.loader.get_summary())

from collections.abc import Generator
from sldatasets.Datasetloader import LSA64, ASLLVD
datasets = {"lsa64": LSA64,
            "asllvd": ASLLVD
            }


class Videodataset(Generator):

    def __init__(self, dataset_id, **kwargs):
        self.loader = self.get_loader(dataset_id, kwargs.get(
            'version'), kwargs.get('path'))
        self.data = self.loader.load_data(**kwargs)

    def send(self, ignored_arg):
        frames, specs = self.data.__next__()
        l = []
        anotation = self.loader.load_annotations()
        anot_index = specs['filename'].split('.')[0]
        try:
            for i, man in enumerate(anotation[anot_index]):
                l.append((frames[i], man))
            return (l, specs)
        except TypeError:
            for f in frames:
                l.append((f, anotation[anot_index]))
            return (l, specs)

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

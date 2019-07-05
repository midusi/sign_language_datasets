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
            frames, specs = self.data.__next__()
            l = []
            for i, human in enumerate(self.npz_file(specs)):
                l.append((frames[i], human))
            return (l, specs)
        except:
            self.throw()

    def npz_file(self, specs):
        return self.loader.load_anotations()[specs['class']+'_' + specs['consultant']+'_'+specs['repetition']]

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

    def walk_through_pre(self, video_tuple):

        npzfile = self.loader.load_anotations(version='pre')
        x = video_tuple[1].split('_')
        index = (int(x[0])-1)*50+(int(x[1])-1)*5+int(x[2])-1
        video = video_tuple[0]
        n, _h, _w, _c = video.shape
        frames = []
        for j in range(0, n):
            frames.append(self.get_tuple(video[j, :], j, index, npzfile))
        return (n for n in frames)

    def get_tuple(self, frame, j, index, npz):
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

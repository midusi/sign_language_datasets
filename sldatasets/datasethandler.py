from pathlib import Path
import os


def process_video(video, e):
    n, h, w, c = video.shape
    frames = []
    for j in range(0, n):
        img = video[j, :]
        frames.append(e.inference(img, True, 4.0)[0])
    return frames


class DatasetHandler(object):
    handler_class = {f'LSA64_raw': 'DH_Lsa64',
                     'LSA64_cut': 'DH_Lsa64',
                     'LSA64_pre': 'DH_Lsa64_pre',
                     }

    def __init__(self, version):
        self.version = version

    def get_my_path(self, root=None):
        # if datasets_path was not specified, use default
        if root is None:
            root = self.get_lib_root()
        return os.path.join(root, self.version)

    def get_lib_root(self):
        return os.path.join(Path.home(), '.sldatasets')

    @staticmethod
    def factory(version):
        try:
            e = DatasetHandler.handler_class[version]
            return globals()[e](version)
        except:
            raise ValueError(
                'version for lsa64("version"), must be "cut", "raw" or "pre"')

    def get_my_url(self):
        raise NotImplementedError

    def get_my_folder(self):
        raise NotImplementedError

    def get_my_file_ext(self):
        raise NotImplementedError

    def redux(self, files, index):
        from os import path as osp
        l = list(filter(lambda f: osp.splitext(f)[1].endswith(
            f'{self.get_my_file_ext()}'), sorted(files)))
        if index is not None:
            return list(filter(lambda f: int(f.split('_')[0]) == index, l))
        else:
            return l

    def get_humans_from_dataset(self, dataset, path=None):
        from tf_pose.estimator import TfPoseEstimator
        from tf_pose.networks import get_graph_path
        import numpy as np
        e = TfPoseEstimator(get_graph_path('cmu'), target_size=(432, 368))
        videos_processed = {}
        print('processing videos wait...')
        for video in dataset:
            videos_processed[video[1]] = process_video(video[0], e)
        videos_processed[video[1]] = process_video(video[0], e)
        outfile = self.get_my_path() if path is None else path
        outfile = os.path.join(outfile, 'dataset_humans.npz')
        np.savez(outfile, **videos_processed)
        print('the file is saved in ', outfile)
        return outfile


class DH_Lsa64(DatasetHandler):

    def get_my_url(self):
        if self.version == 'LSA64_raw':
            return 'https://drive.google.com/uc?id=1C7k_m2m4n5VzI4lljMoezc-uowDEgIUh'
        else:
            return 'https://drive.google.com/uc?id=18VuWBAxHaSBbO7wx57kQVre78FN7GYzQ'

    def get_my_folder(self):
        if self.version == 'LSA64_raw':
            return 'all'
        else:
            return 'all_cut'

    def get_my_file_ext(self):
        return 'mp4'


class DH_Lsa64_pre(DatasetHandler):

    def get_my_url(self):
        return 'https://drive.google.com/uc?id=1yhfPpI2iJzPXyx4C7MYR6IPZC3YuuYaL'

    def get_my_folder(self):
        return 'lsa64_hand_videos'

    def get_my_file_ext(self):
        return 'avi'

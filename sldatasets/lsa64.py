from os import mkdir, path as osp, listdir as osl
from skvideo.io import vread
from zipfile import ZipFile as zf
from sldatasets.datasethandler import DatasetHandler as dh
import gdown
from tempfile import mkdtemp
import logging


class LSA64(object):

    def __init__(self, version="pre"):
        self.x = dh.factory(self.__class__.__name__ + '_' + version)
        self.base_url = self.x.get_my_url()

    def load_videos(self, path):
        path_videos = osp.join(path, self.x.get_my_folder())
        logging.info(f"Loading videos from {path_videos}")
        files = sorted(osl(path_videos))
        for filename in (filter(lambda f: osp.splitext(f)[1].endswith(f'{self.x.get_my_file_ext()}'), files)):
            yield [vread(osp.join(path_videos, filename)), filename]

    def download_and_extract(self, path):

        with zf(self.download()) as zip_ref:

            if zip_ref.testzip() is not None:
                logging.warning("download was incomplete, try again")
            else:
                logging.warning("Extracting videos...please wait...")
                zip_ref.extractall(path)
                zip_ref.close()

    def download(self):
        r = gdown.download(self.x.get_my_url(), f'{mkdtemp()}', False)
        return osp.join(r, osl(r)[0])

    def load_data(self, datasets_path):
        # download dataset (if necessary)

        path = self.x.dataset_path(datasets_path)
        if not osp.exists(path):
            mkdir(path)

        if not osl(path):
            self.download_and_extract(path)
        # load video generator
        return self.load_videos(path)

    def load_anotations(self, dpath=None):
        import h5py
        import numpy as np
        data_dir = self.x.dataset_path(dpath)
        mat_fname = osp.join(data_dir, 'lsa64_positions.mat')
        mat_file = h5py.File(mat_fname, 'r')
        db = mat_file.get('db')
        it = db.keys().__iter__()
        data = {}
        for key in it:
            n = db[key].size
            result = np.empty((n,), dtype=object)
            for j in range(n):
                result[j] = mat_file[db[key][j][0]][()]
            data[key] = result
        outfile = osp.join(data_dir, 'positions.npz')
        np.savez(outfile, **data)
        print('the file is saved in ', outfile)
        return outfile

from os import makedirs, path as osp, listdir as osl
from skvideo.io import vread
from zipfile import ZipFile as zf
from sldatasets.datasethandler import DatasetHandler as dh
import gdown
from tempfile import mkdtemp
import logging


class LSA64(object):

    def __init__(self, version="pre", root_path=None):
        self.x = dh.factory(self.__class__.__name__ + '_' + version)
        self.base_url = self.x.get_my_url()
        self.my_path = self.x.get_my_path(root_path)

    def load_videos(self, index):
        path_videos = osp.join(self.my_path, self.x.get_my_folder())
        logging.info(f"Loading videos from {path_videos}")
        files = list(filter(lambda f: osp.splitext(f)[1].endswith(
            f'{self.x.get_my_file_ext()}'), sorted(osl(path_videos))))
        for filename in self.x.redux(files, index):
            yield [vread(osp.join(path_videos, filename)), filename]

    def download_and_extract(self):

        with zf(self.download()) as zip_ref:

            if zip_ref.testzip() is not None:
                logging.warning("download was incomplete, try again")
            else:
                logging.warning("Extracting videos...please wait...")
                makedirs(self.my_path, exist_ok=True)
                zip_ref.extractall(self.my_path)
                zip_ref.close()

    def download(self):
        r = gdown.download(self.x.get_my_url(), f'{mkdtemp()}', False)
        return osp.join(r, osl(r)[0])

    def load_data(self, index):
        # download dataset (if necessary)
        if (self.my_path != self.x.get_my_path(None)) and not osl(self.my_path):
            self.download_and_extract()
        elif not osp.exists(self.my_path):
            self.download_and_extract()

        return self.load_videos(index)

    def load_anotations(self):
        import h5py
        import numpy as np
        data_dir = self.my_path
        outfile = osp.join(data_dir, 'positions.npz')
        if not osp.exists(outfile):
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
            np.savez(outfile, **data)
        print('the file is saved in ', outfile)
        return outfile

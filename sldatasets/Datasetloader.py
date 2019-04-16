from os import makedirs, path as osp, listdir as osl
import logging


class Datasetloader(object):

    def __init__(self, version="pre", root_path=None):
        logging.info("starting loader")
        from sldatasets.datasethandler import DatasetHandler as dh
        self.x = dh.factory(self.__class__.__name__ + '_' + version)
        self.base_url = self.x.get_my_url()
        self.my_path = self.x.get_my_path(root_path)

    def load_data(self, index):
        # download dataset (if necessary)
        self.check_path(index)

        return self.load_videos(index)

    def check_path(self, index):
        pass

    def download_and_extract(self):
        pass

    def load_videos(self, index):
        pass

    def download(self, index):
        import gdown
        from tempfile import mkdtemp
        dt = mkdtemp()
        for url in self.x.get_my_url():
            r = gdown.download(url, dt, False)
        return osp.join(r, osl(r)[0])


class LSA64(Datasetloader):

    def load_videos(self, index):
        from skvideo.io import vread
        path_videos = osp.join(self.my_path, self.x.get_my_folder())
        logging.info(f"Loading videos from {path_videos}")
        for filename in self.x.redux(osl(path_videos), index):
            yield [vread(osp.join(path_videos, filename)), filename]

    def download_and_extract(self):
        from zipfile import ZipFile as zf
        with zf(self.download()) as zip_ref:

            if zip_ref.testzip() is not None:
                logging.warning("download was incomplete, try again")
            else:
                logging.warning("Extracting videos...please wait...")
                makedirs(self.my_path, exist_ok=True)
                zip_ref.extractall(self.my_path)
                zip_ref.close()

    def download(self):
        import gdown
        from tempfile import mkdtemp
        r = gdown.download(self.x.get_my_url(), f'{mkdtemp()}', False)
        return osp.join(r, osl(r)[0])

    def check_path(self, index):
        if (self.my_path != self.x.get_my_path(None)) and not osl(self.my_path):
            self.download_and_extract()
        elif not osp.exists(self.my_path):
            self.download_and_extract()

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


class Boston(Datasetloader):

    def check_path(self, index):
        word_path = osp.join(self.my_path, index)
        if (self.my_path != self.x.get_my_path(None)) and not osp.exists(self.my_path):
            raise NotADirectoryError
        elif not osp.exists(word_path):
            self.download(index)

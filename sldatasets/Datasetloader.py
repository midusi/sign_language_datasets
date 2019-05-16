from os import makedirs, path as osp, listdir as osl, remove
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
        ref = osp.join(self.my_path, 'partial')
        with open(ref, 'w') as flag_file:
        for url in self.x.get_my_url():
            r = gdown.download(url, dt, False)
            flag_file.write(osp.join(r, osl(r)[0]))
            flag_file.write('\n')

        ref = osp.join(self.my_path, 'downloaded')
        # copy from paartial to dowloaded
        flag_file.close()


class LSA64(Datasetloader):

    def load_videos(self, index):
        from skvideo.io import vread
        path_videos = osp.join(self.my_path, self.x.get_my_folder())
        logging.info(f"Loading videos from {path_videos}")
        for filename in self.x.redux(osl(path_videos), index):
            yield [vread(osp.join(path_videos, filename)), filename]

    def extract(self, ref):
        from zipfile import ZipFile
        with ZipFile(osp.join(ref, osl(ref)[0])) as zip_ref:

            if zip_ref.testzip() is not None:
                logging.warning(
                    "download was incomplete or zipfile is corrupt, try again")
                d_flag = osp.join(self.my_path, 'downloaded')
                remove(d_flag)
            else:
                logging.warning("Extracting videos...please wait...")
                zip_ref.extractall(self.my_path)
                zip_ref.close()
                a = osp.join(self.my_path, 'extracted')
                open(a, 'w').close()

    def download(self):
        import gdown
        from tempfile import mkdtemp
        r = gdown.download(self.x.get_my_url(), f'{mkdtemp()}', False)
        makedirs(self.my_path, exist_ok=True)
        ref = osp.join(self.my_path, 'downloaded')
        with open(ref, 'w') as flag_file:
            flag_file.write(osp.join(r, osl(r)[0]))
            flag_file.close()

    def check_path(self, index):
        d_flag = osp.join(self.my_path, 'downloaded')
        e_flag = osp.join(self.my_path, 'extracted')
        if not osp.exists(d_flag):
            self.download()
        elif not osp.exists(e_flag):
            with open(d_flag, 'r') as ref:
                self.extract(ref.readline())
                ref.close()

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
        d_flag = osp.join(self.my_path, 'downloaded')
        e_flag = osp.join(self.my_path, 'extracted')
        if not osp.exists(d_flag):
            self.download()
        elif not osp.exists(e_flag):
            with open(d_flag, 'r') as ref:
                array = ref.readlines()
                for line in array:
                    zipf = array[].split('\n')[0]
                    self.extract(zipf)
                ref.close()

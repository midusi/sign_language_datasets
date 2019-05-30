from os import makedirs, path as osp, listdir as osl, remove, rename
import logging


class Datasetloader(object):

    def __init__(self, version=None, root_path=None):
        from sldatasets.datasethandler import DatasetHandler as dh
        logging.info("starting loader")
        version = 'pre' if version is None else version
        self.x = dh.factory(self.__class__.__name__ + '_' + version)
        self.base_url = self.x.get_my_url()
        self.my_path = self.x.get_my_path(root_path)

    def load_data(self, index):
        self.check_path()
        return self.load_videos(index)

    def check_path(self):
        d_flag = osp.join(self.my_path, 'downloaded')
        if not osp.exists(d_flag):
            self.download()

    def load_videos(self, index):
        pass

    def download(self):
        makedirs(self.my_path, exist_ok=True)


class LSA64(Datasetloader):

    def load_videos(self, index):
        from skvideo.io import vread
        path_videos = osp.join(self.my_path, self.x.get_my_folder())
        logging.info(f"Loading videos from {path_videos}")
        for filename in self.x.redux(osl(path_videos), index):
            yield [vread(osp.join(path_videos, filename)), self.x.parsed_name(filename)]

    def extract(self):
        from zipfile import ZipFile
        ref = (filter(lambda f: f == self.x.version +
                      '.zip', osl(self.my_path))).__next__()

        with ZipFile(osp.join(self.my_path, ref)) as zip_ref:

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
        super().download()
        import gdown
        gdown.download(self.x.get_my_url(), osp.join(
            self.my_path, self.x.version + '.zip'), False)
        flag = osp.join(self.my_path, 'downloaded')
        open(flag, 'w').close()

    def check_path(self):
        super().check_path()
        e_flag = osp.join(self.my_path, 'extracted')
        if not osp.exists(e_flag):
            self.extract()

    def load_anotations(self):
        outfile = osp.join(self.my_path, 'positions.npz')
        if not osp.exists(outfile):
            self.make_npz(outfile)
        print('the file is saved in ', outfile)
        return outfile

    def make_npz(self, outfile):
        import numpy as np
        import h5py
        mat_fname = osp.join(self.my_path, 'lsa64_positions.mat')
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


class Boston(Datasetloader):

    def download(self):
        super().download()
        import gdown
        partial = osp.join(self.my_path, 'partial')
        last = self.x.get_first(self.my_path)
        if osp.exists(partial):
            with open(partial, 'r') as files_downloaded:
                m = files_downloaded.readlines()
                files_downloaded.close()
            if m:
                last = self.x.get_my_url() + m[-1].split('\n')[0]
        with open(partial, 'a') as flag_file:
            l = self.x.get_urls()
            i = l.index(last)
            if m:
                i = i+1
            for url in l[i:]:
                filename = url.split('/')[-1]
                gdown.download(url, osp.join(self.my_path, filename), False)
                flag_file.write(filename + '\n')
            flag_file.close()
        ref = osp.join(self.my_path, 'downloaded')
        rename(partial, ref)

    def load_videos(self, index):
        from skvideo.io import vread
        logging.info(f"Loading videos from {self.my_path}")
        for filename in self.x.redux(osl(self.my_path), index):
            yield [vread(osp.join(self.my_path, filename)), self.x.parsed_name(filename)]

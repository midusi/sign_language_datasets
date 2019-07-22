from os import makedirs, path as osp, listdir as osl, remove, rename
import logging


class Datasetloader(object):

    def __init__(self, version=None, root_path=None):
        from sldatasets.datasethandler import DatasetHandler as dh
        logging.info("starting loader")
        version = 'pre' if version is None else version
        self.x = dh.factory(self.__class__.__name__ + '_' + version)
        self.my_path = self.x.get_my_path(root_path)

    def load_data(self, **kwargs):
        self.check_path()
        return self.load_videos(self.path_videos(), **kwargs)

    def check_path(self):
        d_flag = osp.join(self.my_path, 'downloaded')
        if not osp.exists(d_flag):
            self.download()
        self.extract_data()

    def extract_data(self):
        e_flag = osp.join(self.my_path, 'extracted')
        if not osp.exists(e_flag):
            self.extract()

    def extract(self):
        pass

    def load_videos(self, path_videos, **kwargs):
        from skvideo.io import vread
        logging.info(f"Loading videos from {path_videos}")
        for filename in self.x.redux(osl(path_videos), **kwargs):
            yield [vread(osp.join(path_videos, filename)), self.x.parsed_name(filename)]

    def download(self):
        makedirs(self.my_path, exist_ok=True)
        self.download_n_flag()

    def download_n_flag(self):
        pass

    def path_videos(self):
        pass

    def get_summary(self):
        c = self.x.word_count(osl(self.path_videos()))
        return {'name': self.__class__.__name__,
                'version': self.x.version,
                'link': self.x.get_my_url(),
                'words': c[0],
                'subjects': c[1],
                'repetitions': c[2]}


class LSA64(Datasetloader):

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

    def path_videos(self):
        return osp.join(self.my_path, self.x.get_my_folder())

    def download_n_flag(self):
        import gdown
        gdown.download(self.x.get_my_url(), osp.join(
            self.my_path, self.x.version + '.zip'), False)
        flag = osp.join(self.my_path, 'downloaded')
        open(flag, 'w').close()

    def load_anotations(self):
        import numpy as np
        outfile = osp.join(self.my_path, 'positions.npz')
        if not osp.exists(outfile):
            from gdown import download
            logging.info(f"Dowloading Positions to {outfile}")
            download(self.x.get_pos_url(), outfile, quiet=False)
        return np.load(outfile)


class Boston(Datasetloader):

    def __init__(self, version=None, root_path=None):
        super().__init__(version, root_path)
        self.videos_path = osp.join(self.my_path, 'videos')
        self.sessions_path = osp.join(self.my_path, 'sessions')
        makedirs(self.sessions_path, exist_ok=True)
        makedirs(self.videos_path, exist_ok=True)
        self.x.set_dai_path(self.my_path)

    def download_n_flag(self):
        partial = osp.join(self.my_path, 'partial')
        last = self.x.get_first()
        m = None
        if osp.exists(partial):
            last, m = self.last_from_partial(partial, last)
        with open(partial, 'a') as flag_file:
            self.download_n_registry(last, m, flag_file)
        ref = osp.join(self.my_path, 'downloaded')
        rename(partial, ref)

    def download_n_registry(self, last, m, flag_file):
        import gdown
        urls = self.x.get_urls()
        i = urls.index(last)
        if m:
            i = i+1
        for url in urls[i:]:
            session, scene = url.split('/')[-2:]
            partial_registry = session+'/'+scene
            gdown.download(url, self.file_path(session, scene), False)
            flag_file.write(partial_registry + '\n')
        flag_file.close()

    def last_from_partial(self, partial, last):
        with open(partial, 'r') as files_downloaded:
            m = files_downloaded.readlines()
            files_downloaded.close()
        if m:
            last = self.x.get_my_url() + m[-2:].split('\n')[0]
        return last, m

    def file_path(self, session, scene):
        session_path = osp.join(self.sessions_path, session)
        makedirs(session_path)
        return osp.join(session_path, scene)

    def extract(self):
        from skvideo.io import vwrite
        from os import walk
        for (session_dir, _j, scenes) in list(walk(self.sessions_path)):
            for scene in scenes:
                scene_dict = self.x.extract_signs_from(
                    osp.join(session_dir, scene))
                for key, value in scene_dict.items():
                    vwrite(osp.join(self.videos_path, key), value)
        a = osp.join(self.my_path, 'extracted')
        open(a, 'w').close()

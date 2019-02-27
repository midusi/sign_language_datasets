from pathlib import Path
import os


class DatasetHandler(object):

    def __init__(self, version):
        self.version = version
        my_path = self.get_my_path()
        os.makedirs(my_path, exist_ok=True)
        os.chdir(my_path)
        self.urls = {'raw': ['https://drive.google.com/uc?id=1C7k_m2m4n5VzI4lljMoezc-uowDEgIUh', 'all', 'mp4'],
                     'cut': ['https://drive.google.com/uc?id=18VuWBAxHaSBbO7wx57kQVre78FN7GYzQ', 'all_cut', 'mp4'],
                     'pre': ['https://drive.google.com/uc?id=1yhfPpI2iJzPXyx4C7MYR6IPZC3YuuYaL', 'lsa64_hand_videos', 'avi'],
                     'prueba': ['https://drive.google.com/uc?id=0B2PnuPB2APN5MDY3NTg2MzUtZGZhOS00YjAwLWJiZTktNGVjYWFjODBjMGQ3', 'prueba', 'docx']}

    def get_lib_root(self):
        return os.path.join(Path.home(), '.lsDatasets')

    def get_my_path(self):
        return os.path.join(f'{self.get_lib_root()}', self.version)

    @staticmethod
    def factory(version):
        try:
            s = 'DH_Lsa64_' + version
            c = globals()[s]
            return c('lsa64_' + version)
        except:
            raise ValueError(
                'version for lsa64("version"), must be "cut", "raw" or "pre"')

    def get_my_url(self):
        return self.urls.get(self.version.split('_')[1])[0]

    def get_my_folder(self):
        return self.urls.get(self.version.split('_')[1])[1]

    def get_my_file_ext(self):
        return self.urls.get(self.version.split('_')[1])[2]


class DH_Lsa64_raw(DatasetHandler):

    def get_my_url(self):
        return 'https://drive.google.com/uc?id=1C7k_m2m4n5VzI4lljMoezc-uowDEgIUh'

    def get_my_folder(self):
        return 'all'

    def get_my_file_ext(self):
        return 'mp4'


class DH_Lsa64_pre(DatasetHandler):

    def get_my_url(self):
        return 'https://drive.google.com/uc?id=1yhfPpI2iJzPXyx4C7MYR6IPZC3YuuYaL'

    def get_my_folder(self):
        return 'lsa64_hand_videos'

    def get_my_file_ext(self):
        return 'avi'


class DH_Lsa64_cut(DatasetHandler):

    # def __init__(self, version):
    #     super(DH_Lsa64_cut, self).__init__(version)

    def get_my_url(self):
        return 'https://drive.google.com/uc?id=18VuWBAxHaSBbO7wx57kQVre78FN7GYzQ'

    def get_my_folder(self):
        return 'all_cut'

    def get_my_file_ext(self):
        return 'mp4'

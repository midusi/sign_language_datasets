from pathlib import Path
import os


class DatasetHandler(object):
    handler_class = {'lsa64_raw': 'DH_Lsa64',
                     'lsa64_cut': 'DH_Lsa64',
                     'lsa64_pre': 'DH_Lsa64_pre',
                     'lsa64_prueba': 'DH_Test'}

    def __init__(self, version):
        self.version = version
        my_path = self.get_my_path()
        os.makedirs(my_path, exist_ok=True)
        os.chdir(my_path)

    def get_lib_root(self):
        return os.path.join(Path.home(), '.lsDatasets')

    def get_my_path(self):
        return os.path.join(f'{self.get_lib_root()}', self.version)

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


class DH_Lsa64(DatasetHandler):

    def get_my_url(self):
        if self.version == 'lsa64_raw':
            return 'https://drive.google.com/uc?id=1C7k_m2m4n5VzI4lljMoezc-uowDEgIUh'
        else:
            return 'https://drive.google.com/uc?id=18VuWBAxHaSBbO7wx57kQVre78FN7GYzQ'

    def get_my_folder(self):
        if self.version == 'lsa64_raw':
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


class DH_Test(DatasetHandler):

    def get_my_url(self):
        return 'https://drive.google.com/uc?id=0B2PnuPB2APN5MDY3NTg2MzUtZGZhOS00YjAwLWJiZTktNGVjYWFjODBjMGQ3'

    def get_my_folder(self):
        return ''

    def get_my_file_ext(self):
        return 'docx'

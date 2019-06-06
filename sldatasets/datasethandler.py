from pathlib import Path
from os import path as osp, rename


class DatasetHandler(object):
    handler_class = {f'LSA64_raw': 'DH_Lsa64',
                     'LSA64_cut': 'DH_Lsa64',
                     'LSA64_pre': 'DH_Lsa64_pre',
                     'Boston_pre': 'DH_Boston_pre'
                     }

    def __init__(self, version):
        self.version = version

    def get_my_path(self, root=None):
        # if datasets_path was not specified, use default
        if root is None:
            root = self.get_lib_root()
        return osp.join(root, self.version)

    def get_lib_root(self):
        return osp.join(Path.home(), '.sldatasets')

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

    def redux(self, files, **kwargs):
        l = list(filter(lambda f: osp.splitext(f)[1].endswith(
            f'{self.get_my_file_ext()}'), sorted(files)))

        def file_filter(self, f, clas, consultant, repetition):
            name = self.parsed_name(f)
            return ((int(name['class']) == int(clas) if clas else True) and
                    (int(name['consultant']) == consultant if consultant else True) and
                    (int(name['repetition']) == repetition if repetition else True))
        l = list(filter(lambda f: file_filter(
            self, f, kwargs.get('index'), kwargs.get('consultant'), kwargs.get('repetition')), l))
        return l

    def parsed_name(self, filename):
        val = filename.split('_')
        return {'class': self.sign_class(val), 'consultant': self.consultant(val)}

    def sign_class(self, parsed):
        return parsed[0]

    def consultant(self, parsed):
        return parsed[1]

    def word_count(self, videos_list):
        class_s = set([])
        consultant_s = set([])
        repetition_s = set([])
        for video in filter(lambda f: osp.splitext(f)[1].endswith(f'{self.get_my_file_ext()}'), videos_list):
            d = self.parsed_name(video)
            class_s.add(d['class'])
            consultant_s.add(d['consultant'])
            self.add_rep(repetition_s, d)
        return [len(class_s), len(consultant_s), len(repetition_s)]

    def add_rep(self, repetition_s, d):
        repetition_s.add(d['repetition'])


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

    def parsed_name(self, filename):
        d = super().parsed_name(filename)
        d['repetition'] = filename.split('_')[2].split('.')[0]
        return d


class DH_Lsa64_pre(DatasetHandler):

    def get_my_url(self):
        return 'https://drive.google.com/uc?id=1yhfPpI2iJzPXyx4C7MYR6IPZC3YuuYaL'

    def get_my_folder(self):
        return 'lsa64_hand_videos'

    def get_my_file_ext(self):
        return 'avi'

    def parsed_name(self, filename):
        d = super().parsed_name(filename)
        v = filename.split('_')
        d['repetition'] = v[2]
        d['hand'] = v[3].split('.')[0]
        return d


class DH_Boston_pre(DatasetHandler):

    def get_my_url(self):
        return 'http://csr.bu.edu/ftp/asl/asllvd/demos/verify_start_end_handshape_annotations//test_auto_move//signs_mov_separ_signers/'

    def get_my_file_ext(self):
        return 'mov'

    def get_first(self, path):
        import openpyxl as pyxl
        url = 'http://www.bu.edu/asllrp/dai-asllvd-BU_glossing_with_variations_HS_information-extended-urls-RU.xlsx'
        self.file_path = osp.join(path, 'index_boston.xlsx')
        if not osp.exists(self.file_path):
            import requests
            resp = requests.get(url)
            with open(self.file_path, 'wb') as f:
                f.write(resp.content)
                f.close()
        wb = pyxl.load_workbook(self.file_path)
        ws = wb['Sheet1']
        # extract first url from xlsx
        return ws.cell(row=4, column=12).value.split('"')[1]

    def get_urls(self):
        import openpyxl as pyxl
        wb = pyxl.load_workbook(self.file_path)
        ws = wb['Sheet1']
        urls = []
        for val in filter(lambda cel: cel.value.startswith('=H'), ws['L']):
            urls.append(val.value.split('"')[1])
        return urls

    def sign_class(self, parsed):
        return parsed[1].split('.')[0]

    def consultant(self, parsed):
        return parsed[0]

    def add_rep(self, repetition_s, d):
        repetition_s.add(None)

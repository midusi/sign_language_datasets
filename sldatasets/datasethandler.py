from pathlib import Path
from os import path as osp, rename


def process_video(video, e):

    n, _h, _w, _c = video.shape
    frames = []
    b = False
    for j in range(0, n):
        img = video[j, :]
        humans = e.inference(img, True, 4.0)
        frames.append(humans)
        if len(humans) != 1:
            b = True
    if b:
        raise InferenceError(frames)
    return frames


class InferenceError(Exception):
    def __init__(self, arg):
        self.args = arg


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

    def redux(self, files, index):
        l = list(filter(lambda f: osp.splitext(f)[1].endswith(
            f'{self.get_my_file_ext()}'), sorted(files)))
        if index is not None:
            return list(filter(lambda f: int(f.split('_')[0]) == index, l))
        else:
            return l

    def parsed_name(self, filename):
        val = filename.split('_')
        return {'class': self.sign_class(val), 'consultant': self.consultant(val)}

    def sign_class(self, parsed):
        return parsed[0]

    def consultant(self, parsed):
        return parsed[1]

    def get_humans_from_dataset(self, dataset, path=None):
        from tf_pose.estimator import TfPoseEstimator
        from tf_pose.networks import get_graph_path
        import numpy as np
        e = TfPoseEstimator(get_graph_path('cmu'), target_size=(432, 368))
        videos_processed = {}
        outfile = self.get_my_path() if path is None else path
        print('processing videos wait...')
        for video in dataset:
            try:
                videos_processed[video[1]] = process_video(video[0], e)
            except InferenceError as ie:
                videos_processed[video[1]] = ie.args
                self.error_handle(ie.args, outfile, video[1])
        outfile = osp.join(outfile, 'dataset_humans.npz')
        np.savez(outfile, **videos_processed)
        print('the file is saved in ', outfile)
        return outfile

    def frames_failed(self, frames):
        index_list = []
        for idx, f in enumerate(frames):
            if len(f) != 1:
                index_list.append(str(idx))
        return index_list

    def error_handle(self, frames, path, video_name):
        with open(osp.join(path, 'processing.log'), 'a') as log:
            log.write('the video ' +
                      video_name + " couldn't be correctly processed, frames failed: ")
            for v in self.frames_failed(frames):
                log.write(v + ' ')
            log.write('\n')
            log.close()
            print('the video ', video_name,
                  " couldn't be correctly processed. processing videos wait...")


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

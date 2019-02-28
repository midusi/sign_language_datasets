import os
#import sys
from skvideo.io import vread
from zipfile import ZipFile as zf
from sldatasets.datasethandler import DatasetHandler as dh
import gdown
from tempfile import mkdtemp
import logging

class LSA64(object):

    def __init__(self, version="pre"):
        print(version)
        print(self.__class__.__name__ + '_' + version)
        self.x = dh.factory(self.__class__.__name__ + '_' + version)
        self.base_url = self.x.get_my_url()

    def load_videos(self,path):
        path_videos = os.path.join(path,self.x.get_my_folder())
        logging.info(f"Loading videos from {path_videos}")
        files = sorted(os.listdir(path_videos))
        for filename in (filter(lambda f: os.path.splitext(f)[1].endswith(f'{self.x.get_my_file_ext()}'), files)):
            yield vread(os.path.join(path_videos, filename))

    def download_and_extract(self,path):

        with zf(self.download()) as zip_ref:

            if zip_ref.testzip() is not None:
                logging.warning("download was incomplete, try again")
            else:
                logging.warning("Extracting videos...please wait...")
                zip_ref.extractall(path)
                zip_ref.close()

    def download(self):
        r = gdown.download(self.x.get_my_url(), f'{mkdtemp()}', False)
        return os.path.join(r, os.listdir(r)[0])

    def load_data(self,datasets_path):
        # download dataset (if necessary)

        path=self.x.dataset_path(datasets_path)
        if not os.path.exists(path):
            os.mkdir(path)

        if not os.listdir(path):
            self.download_and_extract(path)
        # load video generator
        return self.load_videos(path)

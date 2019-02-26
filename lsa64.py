from requests import get
import os
from io import BytesIO
#import sys
from skvideo.io import vread
from zipfile import ZipFile as zf
from dHandler import DatasetHandler as dh
import gdown
from tempfile import mkdtemp


class lsa64(object):

    def __init__(self, version):
        self.x = dh.factory(version)
        self.base_url = self.x.getMyUrl()

        # self.base_url = "https://github.com/tefenet/tp3/archive/master.zip"

    def load_videos(self):
        print("generator for videos in %s" % os.getcwd())
        path_videos = os.path.join(f'{os.getcwd()}', f'{self.x.getMyFolder()}')
        files = sorted(os.listdir(path_videos))
        for filename in (filter(lambda f: os.path.splitext(f)[1].endswith(f'{self.x.getMyFileExt()}'), files)):
            yield vread(os.path.join(path_videos, filename))

    def download_and_extract(self):

        with zf(self.download()) as zip_ref:

            if zip_ref.testzip() is not None:
                print("download was incomplete, try again")
            else:
                print("Extracting videos...please wait...")
                zip_ref.extractall()
                zip_ref.close()

    def download(self):
        r = gdown.download(f'{self.x.getMyUrl()}', f'{mkdtemp()}', False)
        return os.path.join(r, os.listdir(r)[0])
        # with get(self.base_url) as r:
        #     return zf(BytesIO(r.content))

    def load_data(self):
        # download dataset (if necessary)
        if not os.listdir(f'{os.getcwd()}'):
            self.download_and_extract()
        # load video generator
        return self.load_videos()


lsa64('cut').load_data()

# sys.argv[1]

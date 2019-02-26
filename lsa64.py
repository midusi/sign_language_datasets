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
        # try:
        x = dh("lsa64_" + version).getMyUrl()
        if x is not None:
            self.base_url = x
        else:
            raise ValueError(
                'version for lsa64("version"), must be "cut", "raw" or "pre"')
        # except ValueError as er:
        #     print('param must be "cut" or "raw" or "pre"')

        # self.base_url = "https://github.com/tefenet/tp3/archive/master.zip"

    def load_videos(self):
        print("generator for videos in %s" % os.getcwd())
        path_videos = os.path.join(f'{os.getcwd()}', 'all')
        files = sorted(os.listdir(path_videos))
        for filename in (filter(lambda f: os.path.splitext(f)[1].endswith("mp4"), files)):
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
        r = gdown.download(self.base_url, f'{mkdtemp()}', False)
        return os.path.join(r, os.listdir(r)[0])
        # with get(self.base_url) as r:
        #     return zf(BytesIO(r.content))

    def load_data(self):
        # download dataset (if necessary)
        if not os.listdir(f'{os.getcwd()}'):
            self.download_and_extract()
        # load video generator
        return self.load_videos()


lsa64('chof').load_data()

# sys.argv[1]

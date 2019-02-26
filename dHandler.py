from pathlib import Path
import os


class DatasetHandler(object):

    def __init__(self, version):
        self.version = version
        myPath = self.getMyPath()
        os.makedirs(myPath, exist_ok=True)
        os.chdir(myPath)
        # self.url = 'https://drive.google.com/uc?id=0B2PnuPB2APN5MDY3NTg2MzUtZGZhOS00YjAwLWJiZTktNGVjYWFjODBjMGQ3'

    def getLib_Root(self):
        return os.path.join(Path.home(), '.lsDatasets')

    def getMyPath(self):
        return os.path.join(f'{self.getLib_Root()}', self.version)

    @staticmethod
    def factory(version):
        try:
            s = 'DH_Lsa64_' + version
            c = globals()[s]
            return c('lsa64_' + version)
        except:
            raise ValueError(
                'version for lsa64("version"), must be "cut", "raw" or "pre"')

    def getMyUrl(self):
        raise NotImplementedError()

    def getMyFolder(self):
        raise NotImplementedError()

    def getMyFileExt(self):
        raise NotImplementedError()


class DH_Lsa64_raw(DatasetHandler):

    def getMyUrl(self):
        return 'https://drive.google.com/uc?id=1C7k_m2m4n5VzI4lljMoezc-uowDEgIUh'

    def getMyFolder(self):
        return 'all'

    def getMyFileExt(self):
        return 'mp4'


class DH_Lsa64_pre(DatasetHandler):

    def getMyUrl(self):
        return 'https://drive.google.com/uc?id=1yhfPpI2iJzPXyx4C7MYR6IPZC3YuuYaL'

    def getMyFolder(self):
        return 'lsa64_hand_videos'

    def getMyFileExt(self):
        return 'avi'


class DH_Lsa64_cut(DatasetHandler):

    # def __init__(self, version):
    #     super(DH_Lsa64_cut, self).__init__(version)

    def getMyUrl(self):
        return 'https://drive.google.com/uc?id=18VuWBAxHaSBbO7wx57kQVre78FN7GYzQ'

    def getMyFolder(self):
        return 'all_cut'

    def getMyFileExt(self):
        return 'mp4'

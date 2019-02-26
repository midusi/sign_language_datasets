from pathlib import Path
import os


class DatasetHandler(object):

    def __init__(self, version):
        self.version = version
        myPath = self.getMyPath()
        os.makedirs(myPath, exist_ok=True)
        os.chdir(myPath)

    def getLib_Root(self):
        return os.path.join(Path.home(), '.lsDatasets')

    def getMyPath(self):
        return os.path.join(f'{self.getLib_Root()}', self.version)

    def getMyUrl(self):
        urls = {'lsa64_pre': 'https://drive.google.com/file/d/1yhfPpI2iJzPXyx4C7MYR6IPZC3YuuYaL/view?usp=sharing',
                'lsa64_cut': 'https://drive.google.com/uc?id=18VuWBAxHaSBbO7wx57kQVre78FN7GYzQ',
                'lsa64_raw': 'https://drive.google.com/uc?export=download&confirm=UAoR&id=1C7k_m2m4n5VzI4lljMoezc-uowDEgIUh',
                'lsa64_prueba': 'https://drive.google.com/uc?id=0B2PnuPB2APN5MDY3NTg2MzUtZGZhOS00YjAwLWJiZTktNGVjYWFjODBjMGQ3'}

        return urls.get(self.version)

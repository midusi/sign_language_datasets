from tempfile import TemporaryFile
import sldatasets as sld
import numpy as np
dataset = sld.get("lsa64", version="raw")
file_raw = sld.positions_from(dataset, "raw")
dataset = sld.get("lsa64", version="cut")
file_cut = sld.positions_from(dataset, "cut")
npzfile = np.load(file_cut)
print(file_cut.files)

from tempfile import TemporaryFile
import sldatasets as sld
import numpy as np
dataset = sld.get("lsa64", version="raw")
file_raw = sld.positions_from(dataset, "LSA64_raw")
dataset = sld.get("lsa64", version="cut")
file_cut = sld.positions_from(dataset, "LSA64_cut")
npzfile = np.load(file_cut)
print(npzfile.files)

from tempfile import TemporaryFile
import sldatasets as sld
import numpy as np

print("Downloading lsa64 raw")
dataset = sld.get("lsa64", version="raw")
print("processing lsa64 raw")
file_raw = sld.positions_from(dataset, "LSA64_raw")

print("Downloading lsa64 cut")
dataset = sld.get("lsa64", version="cut")
print("processing lsa64 cut")
file_cut = sld.positions_from(dataset, "LSA64_cut")
print("test loading lsa64 cut")
npzfile = np.load(file_cut)
print(npzfile.files)
print("Done")

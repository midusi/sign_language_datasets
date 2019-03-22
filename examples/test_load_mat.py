import sldatasets as sld
import numpy as np

mat_contents = sld.load_anotations()
# npzfile = np.load(mat_contents)
# print(npzfile.files)
# print(npzfile['arr_0'])
print(mat_contents.keys())
print(mat_contents.values())

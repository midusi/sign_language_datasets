import sldatasets as sld
import numpy as np

mat_contents = sld.load_anotations()
npzfile = np.load(mat_contents)
print(npzfile.files)
print(npzfile['class'])

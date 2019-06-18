import sldatasets as sld
import numpy as np


dataset = sld.get("lsa64", version="cut", index=60)
left_60_1_1 = dataset.__next__()
q = sld.walk_through_pre(left_60_1_1)
# do something with q; <generator> with frames & anotations of 060_001_001_left.avi

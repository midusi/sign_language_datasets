import sys
from matplotlib import pyplot as plt
import sldatasets as sld

dataset = sld.get("lsa64",version="raw")
fps = 30.0
video = dataset.__next__()
n, h, w, c = video.shape
for j in range(0, n):
    img = video[j, :]
    plt.imshow(img)
    plt.title(f'Frame {j}')
    plt.pause(1.0/fps)

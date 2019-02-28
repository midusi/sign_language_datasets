from lsa64 import lsa64
import sys
import numpy as np
from matplotlib import pyplot as plt

dataset = lsa64(sys.argv[1]).load_data()
fps = 30.0
video = dataset.__next__()
n, h, w, c = video.shape
for j in range(0, n):
    img = video[j, :]
    plt.imshow(img)
    plt.title(f'Frame {j}')
    plt.pause(1.0/fps)

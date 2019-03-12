import cv2
import tf_pose as raiz
from tf_pose import common
from tf_pose.estimator import TfPoseEstimator
from tf_pose.networks import get_graph_path
import sys
from matplotlib import pyplot as plt
import sldatasets as sld
import os

n=3
# dataset = sld.get("lsa64", version="cut")
# fps = 30.0
# video = dataset.__next__()
# n, h, w, c = video.shape
os.chdir(raiz.__path__[0])
e = TfPoseEstimator(get_graph_path('cmu'), target_size=(432, 368))
for j in range(0, n):
    # img = video[j, :]
    #print ('......estamosss........' , f'{os.getcwd()}')
    img = common.read_imgfile(
        '../tf_pose_data/p1.jpg', None, None)
    humans = e.inference(img)
    image = TfPoseEstimator.draw_humans(img, humans, imgcopy=False)
    fig = plt.figure()
    a = fig.add_subplot(2, 2, 1)
    a.set_title('Result')
    plt.imshow(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
    # plt.title(f'Frame {j}')
    # plt.pause(1.0/fps)
    plt.show()

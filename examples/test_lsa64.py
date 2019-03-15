from tf_pose.estimator import TfPoseEstimator
from tf_pose.networks import get_graph_path
from matplotlib import pyplot as plt
import sldatasets as sld

dataset = sld.get("lsa64", version="cut")
fps = 30.0
video = dataset.__next__()
n, h, w, c = video.shape
e = TfPoseEstimator(get_graph_path('cmu'), target_size=(432, 368))
for j in range(0, n):
    img = video[j, :]    
    humans = e.inference(img, True, 4.0)
    image = TfPoseEstimator.draw_humans(img, humans, imgcopy=False)    
    plt.imshow(image)
    plt.title(f'Frame {j}')
    plt.pause(1.0/fps)
    

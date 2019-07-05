from tf_pose.estimator import TfPoseEstimator
from tf_pose.networks import get_graph_path
from matplotlib import pyplot as plt
import sldatasets as sld

dataset = sld.get("lsa64", version="cut", index=4)
fps = 30.0
data = dataset.__next__()[0]
e = TfPoseEstimator(get_graph_path('cmu'), target_size=(432, 368))
for tup in data:
    img = tup[0]
    humans = e.inference(img, True, 4.0)
    image = TfPoseEstimator.draw_humans(img, humans, imgcopy=False)
    plt.imshow(image)
    plt.title(f'Frame {j}')
    plt.pause(1.0/fps)

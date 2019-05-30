from tf_pose.estimator import TfPoseEstimator
from tf_pose.networks import get_graph_path
from matplotlib import pyplot as plt
import sldatasets as sld

dataset = sld.get("boston")
dataset = sld.get("lsa64", version="raw")
fps = 30.0

video = dataset.__next__()[0]
n, h, w, c = video.shape

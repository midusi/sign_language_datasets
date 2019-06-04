from tf_pose.estimator import TfPoseEstimator
from tf_pose.networks import get_graph_path
from matplotlib import pyplot as plt
import sldatasets as sld

dataset = sld.get("lsa64", version="raw", index=35, consultant=6)
fps = 30.0

video, description = dataset.__next__()
print(video.shape)
print(description)

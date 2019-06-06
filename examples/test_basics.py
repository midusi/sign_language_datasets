import sldatasets as sld

dataset = sld.get("boston")
dataset.summary()
video, description = dataset.__next__()
print(video.shape)
print(description)
dataset = sld.get("lsa64", version="raw")
dataset.summary()
video, description = dataset.__next__()
print(video.shape)
print(description)

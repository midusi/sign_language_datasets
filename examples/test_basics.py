import sldatasets as sld

dataset = sld.get("asllvd")
dataset.summary()
for video, description in dataset:
    print(description)
    frame, frame_annot = video[3]
    print(frame.shape)
    print(frame_annot)
dataset = sld.get("lsa64", version='pre')
dataset.summary()
for video, description in dataset:
    print(description)
    frame, frame_annot = video[3]
    print(frame.shape)
    print(frame_annot)

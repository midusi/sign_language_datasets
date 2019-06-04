import sldatasets as sld
# in progress
video_dataset = sld.get('lsa64', version='raw')
print("test loading lsa64 raw npz positions file")
#npzfile = np.load(video_dataset.get_positions())
# print(npzfile.files)
print("Done")

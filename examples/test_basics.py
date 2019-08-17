import sldatasets as sld

dataset = sld.get("asllvd")
print("dataset summary:")
dataset.summary()
for video, description in dataset:
    print('video description:')
    print(description)
    frame, frame_annot = video[3]
    print('frame shape: ', frame.shape)
    print('estimated body parts (x,y,score): ')
    frame_annot.pretty()
    face = frame_annot.h.get_face_box(640, 480)
    print('face box: ', face)
    print(frame_annot.h.get_upper_body_box(640, 480))
# dataset = sld.get("lsa64", version='pre')
# dataset.summary()
# for video, description in dataset:
#     print(description)
#     frame, frame_annot = video[3]
#     print(frame.shape)
#     print(frame_annot)

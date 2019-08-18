import sldatasets as sld

dataset = sld.get("asllvd", word='Twenty', consultant='liz')
print("dataset summary:")
dataset.summary()
for video, description in dataset:
    print('video description:')
    print(description)
    frame, frame_annot = video[3]
    print('frame shape: ', frame.shape)
    print('estimated body parts (x,y,score): ')
    # this method pretty print a Dictionary that returns the method frame_annot.get()
    frame_annot.pretty()

    face = frame_annot.h.get_face_box(640, 480)
    print('face box: ', face)
    print('upper body box: ', frame_annot.h.get_upper_body_box(640, 480))

print('\n testing lsa64...')
dataset = sld.get("lsa64", version='cut', word=25,
                  consultant=10, repetition=5)
dataset.summary()
for video, description in dataset:
    print(description)
    frame, frame_annot = video[3]
    print('frame shape: ', frame.shape)
    print('estimated body parts (x,y,score): ')
    frame_annot.pretty()

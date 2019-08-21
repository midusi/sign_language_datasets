
from sldatasets.annotations import Human
from os import path as osp
import numpy as np
from sldatasets.annotations import Human as H, Frame_annotation as fa, BodyPart


def positions_mat_to_npz(path=None):
    outfile = osp.join(path, 'positions.npz')
    if not osp.exists(outfile):
        make_npz(outfile, path)
    print('the file is saved in ', outfile)


def make_npz(outfile, path):
    import h5py
    mat_fname = osp.join(path, 'lsa64_positions.mat')
    mat_file = h5py.File(mat_fname, 'r')
    db = mat_file.get('db')
    it = db.keys().__iter__()
    data = {}
    for key in it:
        n = db[key].size
        result = np.empty((n,), dtype=object)
        for j in range(n):
            result[j] = mat_file[db[key][j][0]][()]
        data[key] = result
    dat = {}
    for i in range(3200):
        filename = ''
        for k in ('class', 'subject', 'repetition'):
            value_name = str(int(data[k][i][0][0])).zfill(3) + '_'
            filename += value_name
        dat[filename + 'right'] = data['hand_positions_right'][i][0][0]
        if (data['hand_left_exist_in_frame'][i][0][0] == 1):
            dat[filename + 'left'] = data['hand_positions_left'][i][0][0]
    np.savez(outfile, **dat)


def get_humans_from_dataset(dataset, path=None):
    videos_processed = {}
    outfile = osp.curdir() if path is None else path
    print('processing videos wait...')
    process_dataset(dataset, videos_processed, outfile)
    outfile = osp.join(outfile, 'positions.npz')
    np.savez(outfile, **videos_processed)
    print('the file is saved in ', outfile)


def process_dataset(dataset, videos_processed, outfile):
    data, e = get_estimator(dataset)
    for video in data:
        video_name = video[1]['filename'].split('.')[0]
        try:
            videos_processed[video_name] = process_video(video[0], e)
        except InferenceError as ie:
            videos_processed[video_name] = ie.args
            error_handle(ie.args, outfile, video_name)


def get_estimator(dataset):
    from tf_pose.estimator import TfPoseEstimator
    from tf_pose.networks import get_graph_path
    from itertools import tee
    data, copy = tee(dataset)
    _n, h, w, _c = copy.__next__()[0].shape
    e = TfPoseEstimator(get_graph_path('cmu'), target_size=(w, h))
    return data, e


def frames_failed(annotations):
    index_list = []
    for idx, annot in enumerate(annotations):
        if annot.h.part_count() == 0:
            index_list.append(str(idx))
    return index_list


def error_handle(fr_annot, path, video_name):
    with open(osp.join(path, 'processing.log'), 'a') as log:
        log.write('the video ' +
                  video_name + " couldn't be correctly processed, frames failed: ")
        for v in frames_failed(fr_annot):
            log.write(v + ' ')
        log.write('\n')
        log.close()
        print('the video ', video_name,
              " couldn't be correctly processed. processing videos wait...")


def process_video(video, e):
    n, _h, _w, _c = video.shape
    fr_annot = []
    b = False
    for j in range(0, n):
        img = video[j, :]
        humans = e.inference(img, True, 4.0)
        h = H([])
        if len(humans) != 1:
            b = True
        else:
            h = translate(humans, h)
        fr_annot.append(fa(h))
    if b:
        raise InferenceError(fr_annot)
    return fr_annot


def translate(humans, h):
    body = {}
    for key, part in humans[0].body_parts.items():
        body[key] = BodyPart(part.uidx, part.part_idx,
                             part.x, part.y, part.score)
    h.body_parts = body
    h.score = humans[0].score
    return h


class InferenceError(Exception):
    def __init__(self, arg):
        self.args = arg

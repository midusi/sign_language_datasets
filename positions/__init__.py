
from os import path as osp
import numpy as np


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
    np.savez(outfile, **data)


def get_humans_from_dataset(dataset, path=None):
    from tf_pose.estimator import TfPoseEstimator
    from tf_pose.networks import get_graph_path
    e = TfPoseEstimator(get_graph_path('cmu'), target_size=(432, 368))
    videos_processed = {}
    outfile = osp.curdir() if path is None else path
    print('processing videos wait...')
    for video in dataset:
        try:
            videos_processed[video[1]] = process_video(video[0], e)
        except InferenceError as ie:
            videos_processed[video[1]] = ie.args
            error_handle(ie.args, outfile, video[1])
    outfile = osp.join(outfile, 'dataset_humans.npz')
    np.savez(outfile, **videos_processed)
    print('the file is saved in ', outfile)


def frames_failed(frames):
    index_list = []
    for idx, f in enumerate(frames):
        if len(f) != 1:
            index_list.append(str(idx))
    return index_list


def error_handle(frames, path, video_name):
    with open(osp.join(path, 'processing.log'), 'a') as log:
        log.write('the video ' +
                  video_name + " couldn't be correctly processed, frames failed: ")
        for v in frames_failed(frames):
            log.write(v + ' ')
        log.write('\n')
        log.close()
        print('the video ', video_name,
              " couldn't be correctly processed. processing videos wait...")


def process_video(video, e):
    n, _h, _w, _c = video.shape
    frames = []
    b = False
    for j in range(0, n):
        img = video[j, :]
        humans = e.inference(img, True, 4.0)
        frames.append(humans)
        if len(humans) != 1:
            b = True
    if b:
        raise InferenceError(frames)
    return frames


class InferenceError(Exception):
    def __init__(self, arg):
        self.args = arg

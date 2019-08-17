import positions
import sldatasets as sld
from pathlib import Path
import os.path as osp

example_path = osp.join(Path.home(), '.sldatasets')
# must provide the path of 'lsa64_positions.mat', in this example
# ~/.sldatasets/LSA&$_pre
# a_path = osp.join(example_path, 'LSA64_pre')
# positions.positions_mat_to_npz(osp.join(example_path, 'LSA64_pre'))

# # can provide the destiny path of the npz else current dir will be used, in this example
# # ~/.sldatasets/LSA64_raw
a_path = osp.join(example_path, 'LSA64_raw')
positions.get_humans_from_dataset(
    sld.get('lsa64', version='raw'), a_path)

a_path = osp.join(example_path, 'LSA64_cut')
positions.get_humans_from_dataset(
    sld.get('lsa64', version='cut'), a_path)

a_path = osp.join(example_path, 'ASLLVD_pre')
positions.get_humans_from_dataset(sld.get('asllvd').data, a_path)

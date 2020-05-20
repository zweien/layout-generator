# -*- encoding: utf-8 -*-
"""
Desc      :   convert data format
"""
# File    :   convert.py
# Time    :   2020/04/16 11:15:31
# Author  :   Zweien
# Contact :   278954153@qq.com

from pathlib import Path
import scipy.io as sio
import h5py
import tqdm
from multiprocessing import Pool
from .io import load_mat


def mat2h5(mat_dir, h5_path, keys=("F", "u", "list"), worker=1):
    """Conver mat files to hdf5.

    Args:
        mat_dir (str): mat file dir
        h5_path (str): hdf5 file path
        key (tuple, optional): [description]. Defaults to ("F", "u", "list").
    """
    mat_dir = Path(mat_dir)
    assert mat_dir.is_dir(), "mat_dir must be dir path!"
    fns = list(mat_dir.glob("*.mat"))
    num_fn = len(fns)
    if num_fn == 0:
        return
    mat_shape = get_mat_shape(fns[0])  # {key: shape_tuple}
    with h5py.File(h5_path, "w") as h5_file:
        dataset = {}
        for key, shape in mat_shape.items():
            if key in keys:
                dataset[key] = h5_file.create_dataset(
                    key, shape=(num_fn, *shape)
                )  # shape: (num, element_shape)

        # read form mat and save into h5 ds
        with Pool(worker) as pool:
            results = pool.imap_unordered(load_mat, fns)
            for i, mat in enumerate(
                tqdm.tqdm(results, desc=f"{pool._processes} workers's running")
            ):
                for key in mat_shape.keys():
                    if key in keys:
                        dataset[key][i, :] = mat[key]
        # for i, fn in enumerate(fns):
        #     mat = load_mat(fn)
        #     for key in mat_shape.keys():
        #         if key in keys:
        #             dataset[key][i, :] = mat[key]


def get_mat_shape(mat_fn):
    """get shape of each element of mat file.

    Args:
        mat_fn (str): mat file path

    Returns:
        dict: {key: shape}
    """
    mat = sio.loadmat(mat_fn)
    return {k: v.shape for k, v in mat.items() if not k.startswith("__")}


def get_parser(parser):

    parser.add_argument(
        "-i", "--input", type=str, required=True, help="input dir path"
    )
    parser.add_argument(
        "-o", "--output", type=str, required=True, help="output path"
    )
    parser.add_argument(
        "-m",
        "--mode",
        type=str,
        choices=["mat2h5"],
        default="mat2h5",
        help="converting mode",
    )
    parser.add_argument("--worker", type=int, help="number of workers")
    parser.add_argument("--test", action="store_true", help="test mode")
    return parser

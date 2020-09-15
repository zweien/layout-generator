# -*- encoding: utf-8 -*-
"""
Desc      :   visulaizing layout data.
"""
# File    :   visualize.py
# Time    :   2020/03/29 15:19:17
# Author  :   Zweien
# Contact :   278954153@qq.com


import scipy.io as sio
from functools import partial
import matplotlib.pyplot as plt
from pathlib import Path
import tqdm
from multiprocessing import Pool


def plot_mat(
    mat_path,
    plot=True,
    save=False,
    worker=None,
    figkwargs={"figsize": (12, 5)},
):
    """Plot mat files.

    Arguments:
        mat_path (Path) : mat files path

    Keyword Arguments:
        plot (bool) : whether to show plot (default: (True))
        save (bool or str) : whether to save figure, can be fig path (default: (False))
        figkwargs (dict) : figure kwargs (default: {{'figsize': (12, 5)}})
    """
    mat_path = Path(mat_path)
    assert mat_path.exists(), "Input path does not exist!"
    if mat_path.is_dir():
        plot_dir(mat_path, save, worker)
        return
    mat = sio.loadmat(mat_path)
    xs, ys, u, F = mat["xs"], mat["ys"], mat["u"], mat["F"]

    fig = plt.figure(**figkwargs)
    plt.subplot(121)
    img = plt.pcolormesh(xs, ys, u, shading='auto')
    plt.colorbar(img)
    plt.axis("image")
    plt.title("U")

    plt.subplot(122)
    img = plt.pcolormesh(xs, ys, F, shading='auto')
    plt.colorbar(img)
    plt.axis("image")
    plt.title("F")

    if plot:
        plt.show()
    if save:  # save png
        if save is True:
            img_path = mat_path.with_suffix(".png")
        else:  # save is path
            img_path = Path(save)
            if img_path.is_dir():  # save is dir
                img_path = (img_path / mat_path.name).with_suffix(".png")
        fig.savefig(img_path, dpi=100)
        plt.close()


def plot_dir(path, out, worker):
    """将 mat 数据生成 png 图像

    Arguments:
        path {Path} : dir path
        out {Path} : output dir path
        worker {int} : number of workers
    """
    path = Path(path)
    assert path.is_dir(), "Error! Arg path must be a dir."
    if out is None:
        out = True
    else:
        out = Path(out)
        print(out.absolute())
        if out.exists():
            assert Path(out).is_dir(), "Error! Arg out must be a dir."
        else:
            out.mkdir(parents=True)

    with Pool(worker) as pool:
        plot_mat_p = partial(plot_mat, plot=False, save=out)
        pool_iter = pool.imap_unordered(plot_mat_p, path.glob("*.mat"))
        for _ in tqdm.tqdm(
            pool_iter, desc=f"{pool._processes} workers's running"
        ):
            pass


def get_parser(parser):

    parser.add_argument("-p", "--path", type=str, help="file path")
    parser.add_argument("-o", "--output", type=str, help="output path")
    parser.add_argument(
        "--plot-off", action="store_false", help="turn off plot"
    )
    parser.add_argument(
        "--dir", action="store_true", default=False, help="path is dir"
    )
    parser.add_argument("--worker", type=int, help="number of workers")
    parser.add_argument("--test", action="store_true", help="test mode")
    # TODO 3D version
    return parser

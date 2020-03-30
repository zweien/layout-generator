# -*- encoding: utf-8 -*-
'''
Desc      :   visulaizing layout data.
'''
# File    :   visualize.py
# Time    :   2020/03/29 15:19:17
# Author  :   Zweien
# Contact :   278954153@qq.com


import numpy as np
import scipy.io as sio
from functools import partial
import matplotlib.pyplot as plt
from pathlib import Path
import tqdm
from multiprocessing import Pool


def plot_mat(mat_path, plot=True, save=False, figkwargs={'figsize': (12, 5)}):
    """Plot mat file.

    Arguments:
        mat_path {Path} -- mat file path

    Keyword Arguments:
        plot {bool} -- whether to show plot (default: {True})
        save {bool, str} -- whether to save figure, can be fig path  (default: {False})
        figkwargs {dict} -- figure kwargs (default: {{'figsize': (12, 5)}})
    """
    mat_path = Path(mat_path)
    mat = sio.loadmat(mat_path)
    xs, ys, u, F = mat['xs'], mat['ys'], mat['u'], mat['F']

    fig = plt.figure(**figkwargs)
    plt.subplot(121)
    img = plt.pcolormesh(xs, ys, u)
    plt.colorbar(img)
    plt.axis('image')
    plt.title('u')

    plt.subplot(122)
    img = plt.pcolormesh(xs, ys, F)
    plt.colorbar(img)
    plt.axis('image')
    plt.title('F')

    if plot:
        plt.show()
    if save:
        if save == True:
            img_path = mat_path.with_suffix('.png')
        else:
            img_path = save  # save is path
        fig.savefig(img_path, dpi=100)
        plt.close()


def plot_dir(path, out, worker):
    """将 mat 数据生成 png 图像

    Arguments:
        path {Path} -- dir path
        out {Path} -- output dir path 
        worker {int} -- number of workers
    """
    path = Path(path)
    assert path.is_dir(), "Error! Arg --dir must be a dir."
    if out is None:
        out = True
    else:
        assert Path(out).is_dir(), "Error! Arg --out must be a dir."

    with Pool(worker) as pool:
        plot_mat_p = partial(plot_mat, plot=False, save=out)
        pool_iter = pool.imap_unordered(plot_mat_p, path.glob('*.mat'))
        for it in tqdm.tqdm(pool_iter, desc=f'{pool._processes} workers\'s running'):
            pass


def main():
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument('-p', '--path', type=str, help='file path')
    parser.add_argument('-o', '--output', type=str, help='output path')
    parser.add_argument('--plot-off', action='store_false',
                        help='turn off plot')
    parser.add_argument('--dir', action='store_true',
                        default=False, help='path is dir')
    parser.add_argument('--worker', type=int, help='number of workers')

    # TODO 3D version

    args = parser.parse_args()

    if not args.dir:
        plot_mat(args.path, plot=args.plot_off,
                 save=args.output)  # single file
    else:
        plot_dir(args.path, out=args.output, worker=args.worker)


if __name__ == "__main__":
    main()

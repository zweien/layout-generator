# -*- encoding: utf-8 -*-
'''
@File    :   visualize.py
@Time    :   2020/03/20 23:09:53
@Author  :   Zweien
@Contact :   278954153@qq.com
@Desc    :   None
'''
import numpy as np
import scipy.io as sio
import matplotlib.pyplot as plt
from pathlib import Path



def plot_mat(mat_path, plot=True, save=False, figkwargs={'figsize': (12, 5)}):
    """Plot mat file.
    
    Arguments:
        mat_path {[type]} -- mat file path
    
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

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument('-f', '--file', type=str, help='file path')
    parser.add_argument('-o', '--output', type=str, help='output path')
    parser.add_argument('--plot-off', action='store_false', help='turn off plot')
    args = parser.parse_args()
    
    plot_mat(args.file, plot=args.plot_off, save=args.output)


# -*- encoding: utf-8 -*-
'''
Desc      :   IO helper.
'''
# File    :   io.py
# Time    :   2020/03/29 15:21:56
# Author  :   Zweien
# Contact :   278954153@qq.com


import os
from pathlib import Path
import numpy as np
import scipy.io as sio


def save(options, i, U, xs, ys, F, layout_pos_list, zs=None):
    data_dir = Path(options.data_dir)
    file_name = f'{options.prefix}{i}.mat'
    path = data_dir / file_name
    if options.file_format == 'mat':
        savemat(path, U, xs, ys, F, layout_pos_list, zs=zs)


def savemat(path, U, xs, ys, F, layout_pos_list, zs=None):
    # 组件位置从 1 开始
    zs = zs if zs is not None else []
    data = {'u': U, 'xs': xs, 'ys': ys, 'zs': zs, 'F': F,
            'list': np.array(layout_pos_list) + 1}
    sio.savemat(path, data)


def loadmat(path):
    return sio.loadmat(path)


def layout2matrix(ndim, nx, unit_per_row, powers, layout_pos_list):
    assert ndim in [2, 3]
    F = np.zeros((nx + 1,) * ndim)
    if ndim == 3:
        for i, pos in enumerate(layout_pos_list):
            z = pos // (unit_per_row ** 2)
            y = (pos % (unit_per_row ** 2)) // unit_per_row
            x = pos % unit_per_row
            size = int((nx + 1) / unit_per_row)
            # print(f'x{x}y{y}z{z}size{size}')
            x_slice = slice(size * x, size * (x + 1))
            y_slice = slice(size * y, size * (y + 1))
            z_slice = slice(size * z, size * (z + 1))
            F[x_slice, y_slice, z_slice] = powers[i]
            # print(z_slice)
    else:
        for i, pos in enumerate(layout_pos_list):
            x, y = pos % unit_per_row, pos // unit_per_row
            size = int((nx+1) / unit_per_row)
            x_slice = slice(size * x, size * (x + 1))
            y_slice = slice(size * y, size * (y + 1))
            F[y_slice, x_slice] = powers[i]
    return F

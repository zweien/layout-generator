import os
from pathlib import Path
import numpy as np
import scipy.io as sio


def save(options, i, U, xs, ys, F, layout_pos_list):
    data_dir = Path(options.data_dir)
    file_name = f'{options.prefix}{i}.mat'
    path = data_dir / file_name
    if options.file_format == 'mat':        
        savemat(path, U, xs, ys, F, layout_pos_list)


def savemat(path, U, xs, ys, F, layout_pos_list):
    # 组件位置从 1 开始
    data = {'u': U, 'xs': xs, 'ys': ys, 'F':F, 'list': np.array(layout_pos_list) + 1}
    sio.savemat(path, data)


def loadmat(path):
    return sio.loadmat(path)


def layout2matrix(nx, ny, unit_per_row, power, layout_pos_list):
    F = np.zeros((nx+1, ny+1))
    for pos in layout_pos_list:
        col, row = pos % unit_per_row, pos // unit_per_row
        size_x, size_y = int((nx+1) / unit_per_row), int((ny+1) / unit_per_row)
        col_slice = slice(size_y * col, size_y * (col + 1))
        row_slice = slice(size_x * row, size_x * (row + 1))
        F[row_slice, col_slice] = power
    return F
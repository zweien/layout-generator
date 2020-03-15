import os
from pathlib import Path
import numpy as np
import scipy.io as sio


def save(options, i, U, xs, ys, layout_pos_list):
    data_dir = Path(options.data_dir)
    file_name = f'{options.prefix}{i}.mat'
    path = data_dir / file_name
    if options.file_format == 'mat':        
        savemat(path, U, xs, ys, layout_pos_list)


def savemat(path, U, xs, ys, layout_pos_list):
    # 组件位置从 1 开始
    data = {'u': U, 'xs': xs, 'ys': ys, 'list': np.array(layout_pos_list) + 1}
    sio.savemat(path, data)


def loadmat(path):
    return sio.loadmat(path)
# -*- encoding: utf-8 -*-
'''
@File    :   generator.py
@Time    :   2020/03/13 00:44:27
@Author  :   Zweien
@Contact :   278954153@qq.com
@Desc    :   Main function for generator.
'''

import os
from functools import reduce
import numpy as np
import scipy.io as sio
import tqdm
from .fenics_solver import run_solver, get_mesh_grid
from .utils.configarg import options


def generate_from_cli():

    unit_per_row = int(options.length / options.length_unit)

    possible_n = unit_per_row ** 2

    if options.sampler == 'uniform':
        np.random.seed(options.seed)
        sampler = np.random.choice
    # 叠加原理
    if options.method == 'fenics_additive':
        u_basis = []
        for layout_pos in tqdm.trange(possible_n):
            u = run_solver(options.length, options.length_unit, options.bcs, layout_pos,
                                        options.u_D, options.power, options.nx, options.ny, False)
            u_basis.append(u)
        for i in tqdm.trange(options.sample_n):
            layout_pos_list = sorted(sampler(possible_n, options.unit_n, replace=False))
            u_elt = (u_basis[pos] for pos in layout_pos_list)
            U = reduce(np.add, u_elt)
            xs, ys = get_mesh_grid(options.length, options.nx, options.ny)
            if options.file_format == 'mat':
                savemat(i, U, xs, ys, layout_pos_list)
    # 无叠加原理
    elif options.method == 'fenics':
        for i in tqdm.trange(options.sample_n):
            layout_pos_list = sorted(sampler(possible_n, options.unit_n, replace=False))
            U, xs, ys = run_solver(options.length, options.length_unit, options.bcs, layout_pos_list,
                                        options.u_D, options.power, options.nx, options.ny, True)
            if options.file_format == 'mat':
                savemat(i, U, xs, ys, layout_pos_list)
    print('Completed!')


def savemat(i, U, xs, ys, layout_pos_list):
    if not os.path.isdir(options.data_dir):
        os.mkdir(options.data_dir)
    file_name = f'{options.data_dir}/{options.prefix}{i}'
    sio.savemat(file_name, {'u': U, 'xs': xs, 'ys': ys, 'list': np.array(layout_pos_list) + 1}) # 组件位置从 1 开始

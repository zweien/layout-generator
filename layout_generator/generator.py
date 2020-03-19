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
import tqdm
from .fenics_solver import run_solver, get_mesh_grid
from .utils import io


def generate_from_cli(options):
    """Generate from cli with options.
    
    Arguments:
        options {configargparse.Namespace} -- config options
    """
    unit_per_row = int(options.length / options.length_unit)
    possible_n = unit_per_row ** 2
    np.random.seed(options.seed)
    if options.sampler == 'uniform':
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
            U = reduce(np.add, u_elt) / options.unit_n
            F = io.layout2matrix(options.nx, options.ny, unit_per_row, options.power, layout_pos_list)
            xs, ys = get_mesh_grid(options.length, options.nx, options.ny)
            io.save(options, i, U, xs, ys, F, layout_pos_list)
    # 无叠加原理
    elif options.method == 'fenics':
        for i in tqdm.trange(options.sample_n):
            layout_pos_list = sorted(sampler(possible_n, options.unit_n, replace=False))
            # layout_pos_list = [45]
            U, xs, ys = run_solver(options.length, options.length_unit, options.bcs, layout_pos_list,
                                        options.u_D, options.power, options.nx, options.ny, True)
            F = io.layout2matrix(options.nx, options.ny, unit_per_row, options.power, layout_pos_list)
            io.save(options, i, U, xs, ys, F, layout_pos_list)
    print(f'Completed! Generated {options.sample_n} layouts in {options.data_dir}')





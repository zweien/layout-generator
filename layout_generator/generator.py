# -*- encoding: utf-8 -*-
'''
Desc      :   Main function for generator.
'''
# File    :   generator.py
# Time    :   2020/03/29 15:18:57
# Author  :   Zweien
# Contact :   278954153@qq.com


import os
from functools import reduce
from functools import partial
import numpy as np
import tqdm
from multiprocessing import Pool
from .fenics_solver import run_solver, get_mesh_grid
from .utils import io


def generate_from_cli(options):
    """Generate from cli with options.

    Arguments:
        options {configargparse.Namespace} -- config options
    """
    unit_per_row = int(options.length / options.length_unit)
    possible_n = unit_per_row ** options.ndim
    np.random.seed(options.seed)
    if options.sampler == 'uniform':
        sampler = np.random.choice
    powers = [sampler(options.power, options.unit_n)
              for _ in range(options.sample_n)]
    layout_pos_lists = [sampler(possible_n, options.unit_n, replace=False)
                        for _ in range(options.sample_n)]
    # # 叠加原理
    # if options.method == 'fenics_additive':
    #     u_basis = []
    #     for layout_pos in tqdm.trange(possible_n):
    #         u = run_solver(options.length, options.length_unit, options.bcs, layout_pos,
    #                        0, [1.], options.nx, options.ny, False)
    #         u_basis.append(u)
    #     for i in tqdm.trange(options.sample_n):
    #         layout_pos_list = sorted(
    #             sampler(possible_n, options.unit_n, replace=False))
    #         u_elt = (powers[i] * u_basis[pos]
    #                  for i, pos in enumerate(layout_pos_list))
    #         U = reduce(np.add, u_elt) / options.unit_n + options.u_D
    #         F = io.layout2matrix(options.nx, options.ny,
    #                              unit_per_row, powers, layout_pos_list)
    #         xs, ys = get_mesh_grid(options.length, options.nx, options.ny)
    #         io.save(options, i, U, xs, ys, F, layout_pos_list)
    # 无叠加原理
    if options.method == 'fenics':
        method_fenics_p = partial(method_fenics, options=options,
                                  sampler=sampler, possible_n=possible_n, unit_per_row=unit_per_row, powers=powers, layout_pos_lists=layout_pos_lists)

        # for i in range(options.sample_n):
        #     method_fenics_p(i)
        # multiprocess support
        with Pool(options.worker) as pool:
            pool_it = pool.imap_unordered(
                method_fenics_p, range(options.sample_n))
            for it in tqdm.tqdm(pool_it, desc=f'{pool._processes} workers\'s running',
                                total=options.sample_n, ncols=100):
                pass

    print(
        f'Completed! Generated {options.sample_n} layouts in {options.data_dir}')


def method_fenics(i, options, sampler, possible_n, unit_per_row, powers, layout_pos_lists):

    layout_pos_list = layout_pos_lists[i]
    # print(layout_pos_list)
    F = io.layout2matrix(options.ndim, options.nx,
                         unit_per_row, powers[i], layout_pos_list)
    U, xs, ys, zs = run_solver(options.ndim, options.length, options.length_unit, options.bcs, layout_pos_list,
                               options.u_D, powers, options.nx, coordinates=True, F=F, vtk=options.vtk)

    io.save(options, i, U, xs, ys, F, layout_pos_list, zs)

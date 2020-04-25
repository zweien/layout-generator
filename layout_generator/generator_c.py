# -*- encoding: utf-8 -*-
"""
Desc      :   Main function for generator.
"""
# File    :   generator.py
# Time    :   2020/03/29 15:18:57
# Author  :   Zweien
# Contact :   278954153@qq.com

from functools import partial
import numpy as np
import tqdm
import configargparse
from multiprocessing import Pool, Queue
from .fenics_solver import run_solver, run_solver_c
from .utils import io
from .sampler import continuous


def generate_from_cli(options: configargparse.Namespace):
    """Generate from cli with options.

    Arguments:
        options (configargparse.Namespace): config options
    """
    if options.bcs is None:
        options.bcs = []
    seeds = np.random.randint(np.iinfo(np.int32).max, size=options.worker)
    seeds_q = Queue()
    for seed in seeds:
        seeds_q.put(seed)

    unit_n = len(options.units)
    geometry = ["r"] * unit_n
    task = continuous.get_task(
        geometry_board="s",
        size_board=options.length,
        grid_board=options.nx + 1,
        geometry=geometry,
        size=options.units,
        angle=options.angles,
        intensity=options.powers,
        rad=False,
    )

    # # 叠加原理
    # if options.method == 'fenics_additive':
    #     u_basis = []
    #     for layout_pos in tqdm.trange(possible_n):
    #         u = run_solver(options.length, options.length_unit, options.bcs,
    #                          layout_pos,
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

    if options.method == "fenics":
        # 创建单参数函数

        method_fenics_p = partial(
            method_fenics, options=options, sampler=task.sample_layout_seq
        )

        # for i in range(options.sample_n):
        #     method_fenics_p(i)

        # multiprocess support
        with Pool(
            options.worker, initializer=pool_init, initargs=(seeds_q,)
        ) as pool:
            pool_it = pool.imap(method_fenics_p, range(options.sample_n))
            # for i in pool_it:
            #     print(i)
            for _ in tqdm.tqdm(
                pool_it,
                desc=f"{pool._processes} workers's running",
                total=options.sample_n,
                ncols=100,
            ):
                pass

    print(f"Generated {options.sample_n} layouts in {options.data_dir}")


def pool_init(seeds_q):
    seed = seeds_q.get()
    np.random.seed(seed)


def method_fenics(i, options, sampler):
    """采用 fenics 求解
    """
    F, _ = sampler()
    U, xs, ys, zs = run_solver_c(
        options.ndim,
        options.length,
        options.units,
        options.bcs,
        options.u_D,
        options.powers,
        options.nx,
        F,
        coordinates=True,
    )

    io.save(options, i, U, xs, ys, F)

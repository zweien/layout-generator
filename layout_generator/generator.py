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
from multiprocessing import Pool
from .fenics_solver import run_solver
from .utils import io


def generate_from_cli(options: configargparse.Namespace):
    """Generate from cli with options.

    Arguments:
        options (configargparse.Namespace): config options
    """
    if options.bcs is None:
        options.bcs = []
    options.unit_per_row = int(options.length / options.length_unit)
    possible_n = options.unit_per_row ** options.ndim
    np.random.seed(options.seed)
    if options.sampler == "uniform":
        sampler = np.random.choice
    powers_all = [
        sampler(options.power, options.unit_n) for _ in range(options.sample_n)
    ]  # 每个样本
    layout_pos_lists = [
        sampler(possible_n, options.unit_n, replace=False)
        for _ in range(options.sample_n)
    ]
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
            method_fenics,
            options=options,
            sampler=sampler,
            powers_all=powers_all,
            layout_pos_lists=layout_pos_lists,
        )

        # for i in range(options.sample_n):
        #     method_fenics_p(i)

        # multiprocess support
        with Pool(options.worker) as pool:
            pool_it = pool.imap_unordered(
                method_fenics_p, range(options.sample_n)
            )
            for _ in tqdm.tqdm(
                pool_it,
                desc=f"{pool._processes} workers's running",
                total=options.sample_n,
                ncols=100,
            ):
                pass

    print(f"Generated {options.sample_n} layouts in {options.data_dir}")


def method_fenics(i, options, sampler, powers_all, layout_pos_lists):
    """采用 fenics 求解"""
    layout_pos_list = layout_pos_lists[i]
    # print(layout_pos_list)
    # print(powers)

    # F = io.layout2matrix(
    #     options.ndim,
    #     options.nx,
    #     options.unit_per_row,
    #     powers_all[i],
    #     layout_pos_list,
    # )
    # U, xs, ys, zs = run_solver(
    #     options.ndim,
    #     options.length,
    #     options.length_unit,
    #     options.bcs,
    #     layout_pos_list,
    #     options.u_D,
    #     powers_all[i],
    #     options.nx,
    #     coordinates=True,
    #     F=F,
    #     vtk=options.vtk,
    # )

    F, U, xs, ys, zs = layout_pos_list2temp(
        options, layout_pos_list, powers_all[i]
    )

    io.save(options, i, U, xs, ys, F, layout_pos_list, zs)


def layout_pos_list2temp(
    options: configargparse.Namespace, layout_pos_list: list, powers: list
):
    """Get tempreture field from layout position list.

    Args:
        options (configargparse.Namespace): options must have keys `ndim, length, length_unit, unit_per_row, bcs, u_D, nx`. Note that `nx` here is element number which is node number minus 1.
        layout_pos_list (list): The position starts from 0.
        powers (list): The power for each layout unit. len(layout_pos_list)=len(powers).

    Returns:
        F, U, xs, ys, zs
    """
    if "vtk" not in options:
        options.vtk = False
    F = io.layout2matrix(
        options.ndim,
        options.nx,
        options.unit_per_row,
        powers,
        layout_pos_list,
    )
    U, xs, ys, zs = run_solver(
        options.ndim,
        options.length,
        options.length_unit,
        options.bcs,
        layout_pos_list,
        options.u_D,
        powers,
        options.nx,
        coordinates=True,
        F=F,
        vtk=options.vtk,
    )
    return F, U, xs, ys, zs

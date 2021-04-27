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
from scipy.interpolate import griddata
from multiprocessing import Pool, Queue
from .fenics_solver import run_solver_c
from .utils import io
from .sampler.continuous.utils import get_task, get_task_powers_sampling


def generate_from_cli(options: configargparse.Namespace):
    """Generate from cli with options.

    Arguments:
        options (configargparse.Namespace): config options
    """
    if options.bcs is None:
        options.bcs = []
    np.random.seed(options.seed)
    seeds = np.random.randint(2 ** 32, size=options.worker)
    print(options.worker)
    print(seeds)
    seeds_q: Queue = Queue()
    for seed in seeds:
        seeds_q.put(seed)

    unit_n = len(options.units)
    geometry = ["r"] * unit_n

    positions = np.array([k for k in options.positions])
    if options.positions_type == "coord":
        pass
    elif options.positions_type == "grid":
        positions = positions / (options.nx + 1) * options.length
    else:
        raise LookupError(f"Type {options.positions_type} is not supported!")

    task = get_task_powers_sampling(
        geometry_board="s",
        size_board=options.length,
        grid_board=options.nx + 1,
        geometry=geometry,
        size=options.units,
        angle=options.angles,
        intensity=options.powers,
        rad=False,
        position=positions,
    )
    task.warmup()  # warm up, especially for gibbs

    observation = False
    if options.observation_points is not None:
        observation = True
    # print(options)

    if options.method == "fenics":
        # 创建单参数函数

        method_fenics_p = partial(
            method_fenics,
            options=options,
            sampler=task.sample,
            task=task,
            observation=observation,
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


def method_fenics(i, options, sampler, task, observation=False):
    """采用 fenics 求解"""
    while True:
        F, flag = sampler()
        intensity = task.intensity_sample
        if flag:
            break
    U, xs, ys, zs = run_solver_c(
        options.ndim,
        options.length,
        options.units,
        options.bcs,
        options.u_D,
        intensity,
        options.nx,
        F,
        coordinates=True,
    )

    if observation:
        points = np.array(options.observation_points)
        if options.observation_points_type == "coord":
            pass
        elif options.observation_points_type == "grid":
            points = points / (options.nx + 1) * options.length
        else:
            raise LookupError(
                f"Type {options.observation_points_type} is not supported!"
            )
        temp_points = observe_temperature_of_points(points, xs, ys, U)
    else:
        temp_points = None
    io.save(options, i, U, xs, ys, F, observation=temp_points)


def observe_temperature_of_points(points, xs, ys, U):
    """提取观测点处温度值，若不在网格点上采用双线性插值方法"""

    if not isinstance(points, np.ndarray):
        points = np.array(points)
    temp_points = griddata(
        (xs.ravel(), ys.ravel()),
        U.ravel(),
        points.reshape(-1, 2),
        method="linear",
    )
    return temp_points


def layout_pos2temp(
    options: configargparse.Namespace, pos: list, powers: list
):
    if options.bcs is None:
        options.bcs = []
    task = get_task(
        geometry_board="s",
        size_board=options.length,
        grid_board=options.nx,
        geometry=len(options.units) * "r",
        size=options.units,
        angle=options.angles,
        intensity=options.powers,
        rad=False,
        method=None,
    )
    layout = task.layout_from_pos(pos, powers)
    temp, xs, ys, zs = run_solver_c(
        ndim=options.ndim,
        length=options.length,
        units=options.units,
        bcs=options.bcs,
        u0=options.u_D,
        powers=powers,
        nx=options.nx - 1,
        F=layout,
    )
    return layout, temp

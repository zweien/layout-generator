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
from .fenics_solver import run_solver_c
from .utils import io
from .sampler.continuous.utils import get_task


def generate_from_cli(options: configargparse.Namespace):
    """Generate from cli with options.

    Arguments:
        options (configargparse.Namespace): config options
    """
    if options.bcs is None:
        options.bcs = []
    np.random.seed(options.seed)
    seeds = np.random.randint(2**32, size=options.worker)
    print(seeds)
    seeds_q = Queue()
    for seed in seeds:
        seeds_q.put(seed)

    unit_n = len(options.units)
    geometry = ["r"] * unit_n
    task = get_task(
        geometry_board="s",
        size_board=options.length,
        grid_board=options.nx + 1,
        geometry=geometry,
        size=options.units,
        angle=options.angles,
        intensity=options.powers,
        rad=False,
        method=options.sampler,
    )
    task.warmup()  # warm up, especially for gibbs

    if options.method == "fenics":
        # 创建单参数函数

        method_fenics_p = partial(
            method_fenics, options=options, sampler=task.sample
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

from typing import Sequence
import numpy as np
from layout_generator.sampler.continuous.base import Task, Domain, Components


def get_task(
    geometry_board: str,
    size_board: float,
    grid_board: int,
    geometry: Sequence,
    size: Sequence,
    angle: Sequence,
    intensity: Sequence,
    rad=True,
    method: str = "sequence",
) -> Task:
    """构造布局任务

    Args:
        geometry_board (str): [description]
        size_board (float): [description]
        grid_board (int): [description]
        geometry (Sequence): [description]
        size (Sequence): [description]
        angle (Sequence): [description]
        intensity (Sequence): [description]
        rad (bool, optional): [description]. Defaults to True.
        method (str, optional): [description]. Defaults to "sequence".

    Returns:
        Task: [description]
    """

    domain = Domain(geometry_board, size_board, grid_board)
    components = Components(domain, geometry, size, angle, intensity, rad)
    if method == "sequence":
        from layout_generator.sampler.continuous.sequence_layout_sampling import (
            TaskSeq,
        )

        return TaskSeq(components)
    elif method == "gibbs":
        from layout_generator.sampler.continuous.gibbs_layout_sampling import (
            TaskGibbs,
        )

        return TaskGibbs(components)
    elif method is None:
        return Task(components)
    else:
        raise LookupError("Method {method} does not supported!")


def overlap_rec_rec(u1, a1, b1, u2, a2, b2):
    """
    可同时处理多组组件之间的干涉计算。
    :param : u1, u2 两组件中心点坐标 n*2
             a1, b1 组件1 长、宽的一半 n*1
             a2, b2 组件2 长、宽的一半 n*1
    :return : overlap_area 干涉面积 n*1
    """
    Phi1 = np.minimum(
        np.abs(u1[:, 0].reshape([-1, 1]) - u2[:, 0].reshape([-1, 1]))
        - a1.reshape([-1, 1])
        - a2.reshape([-1, 1]),
        0,
    )
    Phi2 = np.minimum(
        np.abs(u1[:, 1].reshape([-1, 1]) - u2[:, 1].reshape([-1, 1]))
        - b1.reshape([-1, 1])
        - b2.reshape([-1, 1]),
        0,
    )
    overlap_area = (-Phi1) * (-Phi2)
    return overlap_area


def overlap_calculation(location, task: Task, pixel=False):
    """
    给定组件坐标，计算组件之间的干涉量
    :param: location: (n,2)矩阵(numpy型)
            pixel=False 默认输入组件的真实坐标
            pixel=True 输入组件的网格坐标
    :return: overlap: 总干涉量大小 overlap > 0 表示干涉
    """
    # 导入布局问题定义
    # task = Task()

    if pixel:
        comp_size = task.components.realsize_pixel
    else:
        comp_size = task.components.realsize
    comp_num = task.components.number

    u1 = np.array([[0, 0]])
    u2 = np.array([[0, 0]])
    a1 = np.array([[0]])
    b1 = np.array([[0]])
    a2 = np.array([[0]])
    b2 = np.array([[0]])

    for i in range(comp_num - 1):
        temp_u1 = (
            location[i, :].reshape(-1, 2).repeat(comp_num - i - 1, axis=0)
        )
        temp_u2 = location[i + 1 : :, :].reshape(-1, 2)
        temp_a1 = (
            (comp_size[i, 0] / 2)
            .reshape(-1, 1)
            .repeat(comp_num - i - 1, axis=0)
        )
        temp_a2 = (comp_size[i + 1 : :, 0] / 2).reshape(-1, 1)
        temp_b1 = (
            (comp_size[i, 1] / 2)
            .reshape(-1, 1)
            .repeat(comp_num - i - 1, axis=0)
        )
        temp_b2 = (comp_size[i + 1 : :, 1] / 2).reshape(-1, 1)

        u1 = np.append(u1, temp_u1, axis=0)
        u2 = np.append(u2, temp_u2, axis=0)
        a1 = np.append(a1, temp_a1, axis=0)
        b1 = np.append(b1, temp_b1, axis=0)
        a2 = np.append(a2, temp_a2, axis=0)
        b2 = np.append(b2, temp_b2, axis=0)
    overlap_area = overlap_rec_rec(u1, a1, b1, u2, a2, b2)
    return np.sum(overlap_area)

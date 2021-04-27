import numpy as np
from layout_generator.sampler.continuous.base import Task, Components
from layout_generator.sampler.continuous.utils import (
    overlap_calculation,
    overlap_rec_rec,
)


class TaskPowersSampling(Task):
    def __init__(self, components: Components):
        super(TaskPowersSampling, self).__init__(components)

    def sample(self):
        """在给定布局情况下，随机对功率进行采样，获得布局对应的F"""

        intensity = self.sample_intensity()
        location = self.given_position
        return self.location_to_image(location, intensity), True

    def sample_intensity(self):
        """在给定布局情况下，随机对功率进行采样"""

        intensity = []
        for p in self.components.intensity:
            if isinstance(p[0], str):
                if p[0] == "uniform":  # 对功率进行区间内的随机采样
                    if len(p) == 3:  # ["uniform", 10000, 20000]
                        intensity.append(
                            np.random.uniform(low=p[1], high=p[2])
                        )
                    elif (
                        len(p) == 4
                    ):  # ["uniform", 10000, 20000, interval=100]
                        choice = range(p[1], p[2] + 1, p[3])
                        intensity.append(np.random.choice(choice))
                    else:
                        raise ValueError(
                            "The data format of powers is not right."
                        )
                else:
                    raise LookupError(f"Method {p[0]} does not supported!")
            else:
                intensity.append(np.random.choice(p))
        self.intensity_sample = intensity
        return self.intensity_sample

    def location_to_image(self, location, intensity):
        """
        将组件坐标转化为离散的布局图像 (注意存在离散误差)

        Args:
            location : 组件中心点坐标 n*2
            intensity: 每个组件的功率

        Return:
            f_layout : 离散后对应的布局图像 domain.grid * domain.grid
        """
        ele_length = self.domain.size / self.domain.grid
        ele_x = np.arange(ele_length / 2, self.domain.size, ele_length)
        ele_y = ele_x
        f_layout = np.zeros((self.domain.grid, self.domain.grid))

        for i in range(self.domain.grid):
            for j in range(self.domain.grid):
                point = np.array([ele_x[i], ele_y[j]]).reshape(1, 2)
                u1 = np.repeat(point, self.components.number, axis=0)
                a1 = np.zeros((self.components.number, 1))
                b1 = np.zeros((self.components.number, 1))
                u2 = location
                a2 = self.components.realsize[:, 0].reshape(-1, 1) / 2
                b2 = self.components.realsize[:, 1].reshape(-1, 1) / 2
                overlap = overlap_rec_rec(u1, a1, b1, u2, a2, b2)
                # print(overlap)
                if np.max(overlap) > 0:
                    ind = np.argsort(-overlap.reshape(1, -1))  # 按照逆序排列并对应序号
                    f_layout[i, j] = intensity[ind[0, 0]]
        return f_layout


if __name__ == "__main__":
    import time
    import matplotlib.pyplot as plt
    from layout_generator.sampler.continuous.utils import (
        get_task_powers_sampling,
    )
    from config import size, angle, intensity_p, geometry, position

    # np.random.seed(1)

    t1 = time.time()

    grid_board = 200  # 100, 201, 400 ok
    task = get_task_powers_sampling(
        geometry_board="s",
        size_board=0.1,
        grid_board=grid_board,
        geometry=geometry,
        size=size,
        angle=angle,
        intensity=intensity_p,
        rad=True,
        position=position,
    )
    task.warmup()
    print("warm up:", time.time() - t1)
    f_sum = np.zeros((grid_board, grid_board))
    t_0 = time.time()
    n_sample = 1
    for i in range(n_sample):
        f_layout, _ = task.sample_until_success()
        t_1 = time.time()
        print(t_1 - t_0)
        t_0 = t_1
        f_sum += f_layout
    t2 = time.time()
    im = plt.imshow(f_sum / n_sample)
    plt.colorbar(im)
    plt.show()
    overlap = overlap_calculation(task.components.given_position, task)
    print(f"干涉量为 {overlap}, 耗时 {t2 - t1} seconds")
    if overlap < 1e-10:
        print("one feasible layout sample!")

    intensity_sample = set((f_layout.reshape(-1).tolist()))
    print("采样的组件功率为", intensity_sample)
    print(task.intensity_sample)

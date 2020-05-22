import numpy as np
from layout_generator.sampler.continuous.base import Task, Components
from layout_generator.sampler.continuous.utils import (
    overlap_calculation,
    overlap_rec_rec,
)


class TaskGibbs(Task):
    def __init__(self, components: Components):
        super(TaskGibbs, self).__init__(components)

    def gibbs_one_dim(self, index, position):
        """根据吉布斯原理进行单变量的条件采样

        Args:
            index : 条件采样的变量编号 1 - 2 - ... - 2*n
            position : 当前布局组件的位置向量 1*2n (x1, y1, x2, y2,..., xn, yn)

        Returns:
            location : 随机条件采样后的新位置向量 1*2n
            flag_sampling : True - 采样成功
        """
        flag_sampling = True
        samp_comp_index = np.ceil(index / 2).astype(
            int
        )  # (1 ~ self.components.number)
        comp_location = position.reshape(-1, 2)  # 将 1*2n 位置向量转化为 n*2 向量

        flag = index % 2
        if flag == 1:  # x 坐标
            virtual_component_location = np.array(
                [self.domain.size / 2, position[index]]
            )
            virtual_component_size = np.array(
                [
                    self.domain.size,
                    self.components.realsize[samp_comp_index - 1, 1],
                ]
            )
        else:  # y 坐标
            virtual_component_location = np.array(
                [position[index - 2], self.domain.size / 2]
            )
            virtual_component_size = np.array(
                [
                    self.components.realsize[samp_comp_index - 1, 0],
                    self.domain.size,
                ]
            )

        real_component_location = np.delete(
            comp_location, samp_comp_index - 1, axis=0
        )
        real_component_size = np.delete(
            self.components.realsize, samp_comp_index - 1, axis=0
        )

        u1 = virtual_component_location.reshape(-1, 2).repeat(
            self.components.number - 1, axis=0
        )
        a1 = (
            virtual_component_size[0]
            .reshape(-1, 1)
            .repeat(self.components.number - 1, axis=0)
            / 2
        )
        b1 = (
            virtual_component_size[1]
            .reshape(-1, 1)
            .repeat(self.components.number - 1, axis=0)
            / 2
        )
        u2 = real_component_location
        a2 = real_component_size[:, 0].reshape(-1, 1) / 2
        b2 = real_component_size[:, 1].reshape(-1, 1) / 2
        overlap = overlap_rec_rec(u1, a1, b1, u2, a2, b2)

        overlap_interval = np.zeros((1, 2))
        for i in range(self.components.number - 1):
            if overlap[i, 0] > 0:
                x_left = (
                    real_component_location[i, flag - 1]
                    - real_component_size[i, flag - 1] / 2
                )
                x_right = (
                    real_component_location[i, flag - 1]
                    + real_component_size[i, flag - 1] / 2
                )
                overlap_interval = np.append(
                    overlap_interval,
                    np.array([x_left, x_right]).reshape(-1, 2),
                    axis=0,
                )
        overlap_interval = np.delete(overlap_interval, 0, axis=0)
        overlap_interval = overlap_interval[
            np.lexsort(overlap_interval[:, ::-1].T)
        ]  # 按行排序

        # 当区间大于两个时，应该考虑区间的重叠，即先判断重叠再取其并集
        if overlap_interval.shape[0] > 1:
            temp_interval = overlap_interval[0, :].reshape(-1, 2)
            count = 0
            for i in range(1, overlap_interval.shape[0]):
                x1_ub = temp_interval[count, 1]
                x2_lb = overlap_interval[i, 0]
                x2_ub = overlap_interval[i, 1]
                if x2_lb < x1_ub:
                    x1_ub = np.max([x1_ub, x2_ub])
                    temp_interval[count, 1] = x1_ub
                else:
                    temp_interval = np.append(
                        temp_interval,
                        overlap_interval[i, :].reshape(-1, 2),
                        axis=0,
                    )
                    count += 1
            overlap_interval = temp_interval

        flatten_overlap_interval = overlap_interval.reshape(1, -1)
        interval = np.sort(
            np.append(flatten_overlap_interval, [0, self.domain.size])
        )

        # 去除无法放下组件的小区间
        length = len(interval) / 2
        piece_interval = interval.reshape(-1, 2)

        length_interval = piece_interval[:, 1] - piece_interval[:, 0]
        samp_comp_length = self.components.realsize[
            samp_comp_index - 1, flag - 1
        ]
        piece_interval = piece_interval[
            np.arange(0, length)[length_interval > samp_comp_length].astype(
                int
            ),
            :,
        ]

        # 在可采样区间内进行分段均匀随机采样
        num_piece = piece_interval.shape[0]
        if num_piece == 0:
            flag_sampling = False
            print(
                (
                    "No available sampling interval"
                    f"for the {index}-th dimensional variable."
                )
            )
            return position, flag_sampling
        temp1 = (samp_comp_length / 2) * np.ones((num_piece, 1))
        piece_interval = piece_interval + np.append(
            temp1, -temp1, axis=1
        ).reshape(-1, 2)
        length_interval = piece_interval[:, 1] - piece_interval[:, 0]
        sum_length = np.sum(length_interval)

        temp = np.random.rand()
        temp_len = temp * sum_length
        for i in range(num_piece):
            temp_low = np.sum(length_interval[0:i])
            temp_high = np.sum(length_interval[0 : i + 1])
            if (temp_len >= temp_low) and (temp_len <= temp_high):
                x_samp_index = piece_interval[i, 0] + (temp_len - temp_low)
        location = position
        location[index - 1] = x_samp_index
        return location, flag_sampling

    def warmup(self, initial_position=None, burn_in_period=1000):
        """使得Gibbs采样达到细致平稳条件"""

        # 可输入初始状态，否则可自动设置全 0
        if initial_position is None:
            self.position = np.zeros(2 * self.components.number)
        else:
            self.position = initial_position

        for i in range(burn_in_period):
            for j in range(2 * self.components.number):
                self.position, flag = self.gibbs_one_dim(j + 1, self.position)
                if flag is False:
                    print(
                        (
                            "Sorry! Please input"
                            f"anther initial position. (i = {i})"
                        )
                    )
        print(
            (
                f"After {burn_in_period} iterations, "
                "the gibbs layout sampling process has almost reached a"
                "steady state. You can go to next step"
                "for random layout sampling."
            )
        )

    def sample(self):
        """通过Gibbs采样原理获得一组随机布局"""

        for i in range(2 * self.components.number):
            self.position, flag = self.gibbs_one_dim(i + 1, self.position)
            if flag is False:
                print("Sorry! Please retry.")
                return None
        self.location = self.position.reshape(-1, 2)
        return self.location_to_image(self.location), True

    def location_to_image(self, location):
        """
        将组件坐标转化为离散的布局图像 (注意存在离散误差)

        Args:
            location : 组件中心点坐标 n*2

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
                    f_layout[i, j] = self.components.intensity[ind[0, 0]]
        return f_layout


if __name__ == "__main__":
    import time
    import matplotlib.pyplot as plt
    from layout_generator.sampler.continuous.utils import get_task
    from config import size, angle, intensity, geometry

    np.random.seed(1)

    t1 = time.time()

    grid_board = 200  # 100, 201, 400 ok
    task = get_task(
        geometry_board="s",
        size_board=0.1,
        grid_board=grid_board,
        geometry=geometry,
        size=size,
        angle=angle,
        intensity=intensity,
        method="gibbs",
    )
    task.warmup()
    print("warm up:", time.time() - t1)
    f_sum = np.zeros((grid_board, grid_board))
    t_0 = time.time()
    n_sample = 1
    for i in range(n_sample):
        f_layout, _ = task.sample()
        t_1 = time.time()
        print(t_1 - t_0)
        t_0 = t_1
        f_sum += f_layout
    t2 = time.time()
    im = plt.imshow(f_sum / n_sample)
    plt.colorbar(im)
    plt.show()
    overlap = overlap_calculation(task.location, task)
    print(f"干涉量为 {overlap}, 耗时 {t2 - t1} seconds")
    if overlap < 1e-10:
        print("one feasible layout sample!")

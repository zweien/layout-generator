import numpy as np
from .base import Components, Task
from .utils import overlap_calculation


class TaskSeq(Task):
    """顺序布局任务"""

    def __init__(self, components: Components):
        self.domain = components.domain
        self.components = components
        self.location = np.zeros((components.number, 2))
        self.angle = components.angle

    def sample(self, sequence=None):
        """按顺序随机摆放组件

        Args:
            sequence (Iterable, optional): 摆放顺序. Defaults to None.

        Returns:
            f_layout, flag: 布局图像, 是否可行
        """
        flag = True
        # 默认顺序以组件面积大小
        if sequence is None:
            sequence = list(reversed(np.argsort(self.components.real_area)))

        f_layout = np.zeros([self.domain.grid, self.domain.grid])

        location = np.zeros([self.components.number, 2])

        # 初始化组件势能矩阵(APF)均为0
        component_APF = np.zeros(
            [
                self.domain.grid + 1,
                self.domain.grid + 1,
                self.components.number,
            ]
        )
        # domain_APF = np.ones([self.domain.grid + 1, self.domain.grid + 1])

        for i in range(self.components.number):
            index = sequence[i]
            # 初始化布局区域APF
            domain_APF = np.ones([self.domain.grid + 1, self.domain.grid + 1])

            # 根据需要摆放的组件 index 将 domain_APF 中可行域赋值为 0
            dx = self.components.realsize_pixel[index, 0].astype(np.int)
            dy = self.components.realsize_pixel[index, 1].astype(np.int)
            x_lb = self.components.posx_pixel_lb[index].astype(np.int)
            x_ub = self.components.posx_pixel_ub[index].astype(np.int)
            y_lb = self.components.posy_pixel_lb[index].astype(np.int)
            y_ub = self.components.posy_pixel_ub[index].astype(np.int)
            domain_APF[(x_lb) : (x_ub + 1), (y_lb) : (y_ub + 1)] = np.zeros(
                [x_ub - x_lb + 1, y_ub - y_lb + 1]
            )

            component_APF_dilation = component_APF
            # 首先确定即将摆放组件与已知摆放组件的闵可夫斯基和区域，标为不可行域
            if i > 0:
                for j in range(i):
                    index1 = sequence[j]
                    dx1 = self.components.realsize_pixel[index1, 0].astype(
                        np.int
                    )
                    dy1 = self.components.realsize_pixel[index1, 1].astype(
                        np.int
                    )
                    row1 = location[index1, 0].astype(np.int)
                    col1 = location[index1, 1].astype(np.int)
                    # 画出不可行域和布局区域的边界的交集
                    tempx_lb = np.max([0, row1 - dx1 / 2 - dx / 2 + 1]).astype(
                        np.int
                    )
                    tempx_ub = np.min(
                        [self.domain.grid, row1 + dx1 / 2 + dx / 2 - 1]
                    ).astype(np.int)
                    tempy_lb = np.max([0, col1 - dy1 / 2 - dy / 2 + 1]).astype(
                        np.int
                    )
                    tempy_ub = np.min(
                        [self.domain.grid, col1 + dy1 / 2 + dy / 2 - 1]
                    ).astype(np.int)
                    component_APF_dilation[
                        tempx_lb : tempx_ub + 1,
                        tempy_lb : tempy_ub + 1,
                        index1,
                    ] = np.ones(
                        [tempx_ub - tempx_lb + 1, tempy_ub - tempy_lb + 1]
                    )

            # 取布局区域的可行域和组件势能的可行域的交集
            feasible_domain_APF = domain_APF + np.sum(
                component_APF_dilation, axis=2
            )

            # 矩阵中数值为0的网格点均可以作为即将摆放组件的中心位置点
            feasible_index_x, feasible_index_y = np.where(
                feasible_domain_APF == 0
            )
            if feasible_index_x.shape[0] == 0:
                print(
                    "An infeasible layout. Please run again!\
                        (This is very rare, lucky U!)"
                )
                flag = False
                return
            choose_index = np.random.randint(
                0, feasible_index_x.shape[0], size=1, dtype="int"
            )
            row = feasible_index_x[choose_index][0]
            col = feasible_index_y[choose_index][0]
            location[index, :] = [row, col]

            f_layout[
                (row - dx // 2) : (row + dx // 2),
                (col - dy // 2) : (col + dy // 2),
            ] = self.components.intensity[index] * np.ones([dx, dy])
            component_APF[
                (row - dx // 2) : (row + dx // 2 + 1),
                (col - dy // 2) : (col + dy // 2 + 1),
                index,
            ] = np.ones([dx + 1, dy + 1])
        self.location = (location / self.domain.grid) * self.domain.size
        # f_layout = f_layout.transpose()[::-1, :]
        return f_layout, flag


if __name__ == "__main__":
    import time
    import matplotlib.pyplot as plt
    from .utils import get_task
    from .config import geometry, angle, intensity, size

    np.random.seed(1)
    # sequence = np.random.choice(range(12), size=12, replace=False)

    t1 = time.time()

    grid_board = 201  # 100, 201, 400 ok
    task = get_task(
        geometry_board="s",
        size_board=0.1,
        grid_board=grid_board,
        geometry=geometry,
        size=size,
        angle=angle,
        intensity=intensity,
        method="sequence",
    )
    f_sum = np.zeros((grid_board, grid_board))
    n_sample = 1
    for i in range(n_sample):
        f_layout, flag = task.sample()
        f_sum += f_layout
    t2 = time.time()
    im = plt.imshow(f_sum / n_sample)
    plt.colorbar(im)
    plt.show()
    overlap = overlap_calculation(task.location, task)
    print(f"干涉量为 {overlap}, 耗时 {t2 - t1} seconds")
    if overlap < 1e-10:
        print("one feasible layout sample!")

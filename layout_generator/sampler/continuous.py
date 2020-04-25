import numpy as np
import matplotlib.pyplot as plt
from typing import Optional, Sequence


class Domain:
    """布局区域信息"""

    def __init__(self, geometry="s", size=0.1, grid=200):
        self.geometry = geometry  # 定义布局区域的形状 s-square
        self.size = size  # unit: m
        self.grid = grid  # 定义划分网格数量


class Components:
    """组件信息"""

    def __init__(
        self,
        domain: Domain,
        geometry: Optional[Sequence],
        size: Optional[Sequence],
        angle: Optional[Sequence],
        intensity: Optional[Sequence],
        rad=True,
    ):
        assert (
            len(size) == len(intensity) == len(angle) == len(geometry)
        ), "Size, intensity, angle and geometry must have the same length."
        self.domain = domain
        # ###################### user defines components here #########
        # 's': square 'r': rectangle
        self.geometry = geometry
        self.number = len(geometry)
        # 先写长边，再写短边，长边与x轴方向的夹角为其摆放角度
        # 例如某组件 x方向的边长 0.1，y方向的边长为 0.2，故其size=[0.2 0.1],angle = pi/2
        # the length and width of components, unit : m
        self.size = np.array(size)

        # the angle of placement
        
        self.angle = np.array(angle)
        if not rad:
            self.angle = self.angle / 180 * np.pi

        # heat disapation power: W
        self.intensity = np.array(intensity)
        # ###################### user defines components here ###########

        self.size_pixel = (self.size / domain.size) * domain.grid
        self.intensity_norm = self.intensity / np.max(
            self.intensity
        )  # normalized

        # 计算旋转角度以后对应  x 轴边长，y 轴边长
        self.realsize = (
            np.reshape(np.cos(self.angle), [-1, 1]) * self.size
            + np.reshape(np.sin(self.angle), [-1, 1]) * self.size[:, ::-1]
        )
        self.realsize_pixel = (self.realsize / domain.size) * domain.grid

        # 组件坐标x,y的上下界
        self.posx_lb = self.realsize[:, 0] / 2
        self.posx_ub = domain.size - self.realsize[:, 0] / 2
        self.posy_lb = self.realsize[:, 1] / 2
        self.posy_ub = domain.size - self.realsize[:, 1] / 2
        # 按照 [x1,y1,x2,y2, ..., xn, yn]顺序展开
        self.pos_lb = np.zeros([1, 2 * self.number])
        self.pos_ub = np.zeros([1, 2 * self.number])
        for i in range(self.number):
            self.pos_lb[0, 2 * i : 2 * i + 2] = np.array(
                [self.posx_lb[i], self.posy_lb[i]]
            ).reshape(1, 2)
            self.pos_ub[0, 2 * i : 2 * i + 2] = np.array(
                [self.posx_ub[i], self.posy_ub[i]]
            ).reshape(1, 2)

        self.posx_pixel_lb = (self.posx_lb / domain.size) * domain.grid
        self.posy_pixel_lb = (self.posy_lb / domain.size) * domain.grid
        self.posx_pixel_ub = (self.posx_ub / domain.size) * domain.grid
        self.posy_pixel_ub = (self.posy_ub / domain.size) * domain.grid
        self.pos_pixel_lb = (self.pos_lb / domain.size) * domain.grid
        self.pos_pixel_ub = (self.pos_ub / domain.size) * domain.grid

    @property
    def real_area(self):
        """组件实际面积 real_x*real_y"""
        return np.prod(self.realsize, axis=1)


class Task:
    """布局任务"""

    def __init__(self, components: Components):
        self.domain = components.domain
        self.components = components
        self.location = np.zeros((components.number, 2))
        self.angle = components.angle

    def sample_layout_seq(self, sequence=None):
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


def get_task(
    geometry_board: str,
    size_board: float,
    grid_board: int,
    geometry: Sequence,
    size: Sequence,
    angle: Sequence,
    intensity: Sequence,
    rad=True,
) -> Task:
    """构造连续布局任务

    Args:
        geometry_board (str): [description]
        size_board (float): [description]
        grid_board (int): [description]
        geometry (Sequence): [description]
        size (Sequence): [description]
        angle (Sequence): [description]
        intensity (Sequence): [description]

    Returns:
        Task: [description]
    """
    domain = Domain(geometry_board, size_board, grid_board)
    components = Components(domain, geometry, size, angle, intensity, rad)
    task = Task(components)

    return task


if __name__ == "__main__":
    import time

    np.random.seed(1)
    # sequence = np.random.choice(range(12), size=12, replace=False)

    t1 = time.time()

    geometry = [
        "s",
        "s",
        "s",
        "s",
        "s",
        "s",
        "s",
        "s",
        "r",
        "r",
        "r",
        "s",
    ]
    size = [
        [0.01, 0.01],
        [0.01, 0.01],
        [0.01, 0.01],
        [0.01, 0.01],
        [0.01, 0.01],
        [0.01, 0.01],
        [0.01, 0.01],
        [0.01, 0.01],
        [0.02, 0.01],
        [0.02, 0.01],
        [0.02, 0.01],
        [0.02, 0.02],
    ]
    angle = [0, 0, 0, 0, 0, 0, 0, 0, 0, np.pi / 2, np.pi / 2, 0]
    intensity = [
        4000,
        6000,
        8000,
        10000,
        10000,
        14000,
        16000,
        20000,
        8000,
        16000,
        10000,
        14000,
    ]

    task = get_task(
        geometry_board="s",
        size_board=0.1,
        grid_board=200,
        geometry=geometry,
        size=size,
        angle=angle,
        intensity=intensity,
    )
    f_sum = np.zeros((200, 200))
    n_sample = 1
    for i in range(n_sample):
        f_layout, flag = task.sample_layout_seq()
        f_sum += f_layout
    t2 = time.time()
    im = plt.imshow(f_sum / n_sample)
    plt.colorbar(im)
    plt.show()
    overlap = overlap_calculation(task.location, task)
    print(f"干涉量为 {overlap}, 耗时 {t2 - t1} seconds")
    if overlap < 1e-10:
        print("one feasible layout sample!")

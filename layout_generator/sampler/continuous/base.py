import numpy as np
from typing import Sequence


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
        geometry: Sequence,
        size: Sequence,
        angle: Sequence,
        intensity: Sequence,
        rad=True,
        position: np.ndarray = None,
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
        # 角度 -> 弧度
        if not rad:
            self.angle = self.angle / 180 * np.pi

        # heat disapation power: W
        self.intensity = [
            (p if isinstance(p, list) else [p]) for p in intensity
        ]

        # define the given position from yaml file
        if position is not None:
            assert len(position) == self.number
            self.given_position = position
        else:
            self.given_position = position
        # ###################### user defines components here ###########

        self.size_pixel = np.rint((self.size / domain.size) * domain.grid)
        # self.intensity_norm = self.intensity / np.max(
        #     self.intensity
        # )  # normalized

        # 计算旋转角度以后对应  x 轴边长，y 轴边长
        self.realsize = (
            np.reshape(np.cos(self.angle), [-1, 1]) * self.size
            + np.reshape(np.sin(self.angle), [-1, 1]) * self.size[:, ::-1]
        )
        self.realsize_pixel = np.rint(
            (self.realsize / domain.size) * domain.grid
        )

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

        self.posx_pixel_lb = np.rint(
            (self.posx_lb / domain.size) * domain.grid
        )
        self.posy_pixel_lb = np.rint(
            (self.posy_lb / domain.size) * domain.grid
        )
        self.posx_pixel_ub = np.rint(
            (self.posx_ub / domain.size) * domain.grid
        )
        self.posy_pixel_ub = np.rint(
            (self.posy_ub / domain.size) * domain.grid
        )
        self.pos_pixel_lb = np.rint((self.pos_lb / domain.size) * domain.grid)
        self.pos_pixel_ub = np.rint((self.pos_ub / domain.size) * domain.grid)

    @property
    def real_area(self):
        """组件实际面积 real_x*real_y"""
        return np.prod(self.realsize, axis=1)

    def __len__(self):
        return self.number


class Task:
    """布局任务"""

    def __init__(self, components: Components):
        self.domain = components.domain
        self.components = components
        self.location = np.zeros((components.number, 2))
        self.angle = components.angle
        self.given_position = components.given_position
        self.intensity_sample = []

        if self.given_position is not None:
            if self.is_overlaping(self.given_position):
                raise ValueError(
                    "Overlap happened! Input another layout (Arg: positions)."
                )

    def sample(self, *args):
        raise NotImplementedError

    def sample_until_success(self, *args):
        while True:
            f_layout, flag = self.sample(*args)
            if flag:
                break
        return f_layout, flag

    def warmup(self, *args):
        pass

    def layout_from_pos(self, pos: list, powers: list):
        """Get layout matrix from position

        Args:
            pos (list): position list, each element is (x, y) position
        """
        assert len(pos) == len(self.components)
        assert len(powers) == len(self.components)
        # TODO 给出每个组件具体位置时，生成对应 layout 图像
        # location = np.array(pos, dtype=np.float32)
        # intensity = np.array(powers, dtype=np.float32)
        location = np.array([k for k in pos])
        intensity = np.array([k for k in powers])

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

    def is_overlaping(self, pos):
        """Check if the components at pos is overlaping

        Args:
            pos (list): position list, each element is (x, y) position
        """
        assert len(pos) == len(self.components)

        # TODO 判断给定位置的组件是否重叠
        location = np.array(pos)
        overlap = overlap_calculation(location, self)
        return False if overlap < 1e-10 else True


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

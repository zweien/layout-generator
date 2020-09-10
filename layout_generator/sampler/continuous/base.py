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
        self.realsize_pixel = np.rint((self.realsize / domain.size) * domain.grid)

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

        self.posx_pixel_lb = np.rint((self.posx_lb / domain.size) * domain.grid)
        self.posy_pixel_lb = np.rint((self.posy_lb / domain.size) * domain.grid)
        self.posx_pixel_ub = np.rint((self.posx_ub / domain.size) * domain.grid)
        self.posy_pixel_ub = np.rint((self.posy_ub / domain.size) * domain.grid)
        self.pos_pixel_lb = np.rint((self.pos_lb / domain.size) * domain.grid)
        self.pos_pixel_ub = np.rint((self.pos_ub / domain.size) * domain.grid)

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

    def sample(self, *args):
        raise NotImplementedError

    def warmup(self, *args):
        pass

# -*- encoding: utf-8 -*-
'''
Desc      :   solver for layout-generator equation.
'''
# File    :   fenics_solver.py
# Time    :   2020/03/29 15:16:48
# Author  :   Zweien
# Contact :   278954153@qq.com


from typing import List, Callable, Union
from fenics import *

set_log_level(40)  # ERROR = 40
TOL = 1e-14


class Source(UserExpression):
    """热源布局"""

    def __init__(self, layouts, length, length_unit, powers):
        """

        Arguments:
            layouts {list or int} -- 组件摆放位置
            length {float} -- 布局板尺寸
            length_unit {float} -- 组件尺寸
        """
        super().__init__(self)
        self.layout_list = layouts if isinstance(layouts, list) else [layouts]
        self.length = length
        self.length_unit = length_unit
        self.n = length / length_unit  # unit_per_row
        self.powers = powers

    def eval(self, value, x):
        value[0] = self.get_source(x)

    def get_source(self, x):
        for _, (l, power) in enumerate(zip(self.layout_list, self.powers)):
            lx, ly = l % self.n, l // self.n
            if (self.length_unit * lx <= x[0] <= self.length_unit * (lx + 1)) \
                    and (self.length_unit * ly <= x[1] <= self.length_unit * (ly + 1)):
                return power

        return 0

    def value_shape(self):
        return ()


class SourceF(UserExpression):

    def __init__(self, F, length):
        """

        Args:
            F (ndarray): 热源矩阵，2d or 3d
            length (float): 板边长
        """
        super().__init__(self)
        self.F = F
        self.ndim = F.ndim
        self.length = length

    def eval(self, value, x):
        value[0] = self.get_source(x)

    def get_source(self, x):
        """由预生成的 F 获取热源函数值 f(x).

        Args:
            x : 坐标

        Returns:
            float: 热源函数值 f(x)
        """
        assert self.ndim in [2, 3]
        n = self.F.shape[0]
        if self.ndim == 2:
            xx = int(x[0] / self.length * (n - 1))
            yy = int(x[1] / self.length * (n - 1))
            return self.F[yy, xx]
        xx = int(x[0] / self.length * (n - 1))
        yy = int(x[1] / self.length * (n - 1))
        zz = int(x[2] / self.length * (n - 1))
        return self.F[zz, yy, xx]

    def value_shape(self):
        return ()


class LineBoundary():
    """线段边界

    Args:
        line (list): 表示边界的线段，格式为 [[起点x, 起点y], [终点x, 终点y]]
    """

    def __init__(self, line):

        self.line = line
        assert len(line) == 2, "线段包含两个点"
        assert len(line[0]) == 2 and len(line[1]) == 2, "二维点"

    def get_boundary(self):
        """构造 fenics 所需 bc 函数

        Returns:
            function: fenics 所需 bc
        """
        def boundary(x, on_boundary):
            if on_boundary:
                (lx, ly), (rx, ry) = self.line
                if (lx - TOL <= x[0] <= rx + TOL) and (ly - TOL <= x[1] <= ry + TOL):
                    return True
            return False
        return boundary


class RecBoundary():
    """线段边界

    Args:
        rec (list): 表示边界的矩形，格式为 [[起点x, 起点y, 起点z], [终点x, 终点y, 终点z]]
    """

    def __init__(self, rec):
        self.rec = rec
        assert len(rec) == 2, "线段必须包含两个点"
        assert len(rec[0]) == 3 and len(rec[1]) == 3, "必须为三维点"

    def get_boundary(self):
        """构造 fenics 所需 bc 函数

        Returns:
            function: fenics 所需 bc
        """
        def boundary(x, on_boundary):
            if on_boundary:
                (lx, ly, lz), (rx, ry, rz) = self.rec
                if (lx - TOL <= x[0] <= rx + TOL) and (ly - TOL <= x[1] <= ry + TOL) \
                        and (lz - TOL <= x[2] <= rz + TOL):
                    return True
            return False
        return boundary


def solver(f, u_D, bc_funs, ndim, length, nx, ny, nz=None, degree=1):
    """Fenics 求解器

    Args:
        f (Expression): [description]
        u_D (Expression): [description]
        bc_funs (List[Callable]): [description]
        ndim (int): [description]
        length (float): [description]
        nx (int): [description]
        ny (int): [description]
        nz (int, optional): [description]. Defaults to None.
        degree (int, optional): [description]. Defaults to 1.

    Returns:
        Function: 解 u
    """

    mesh = get_mesh(length, nx, ny, nz)
    V = FunctionSpace(mesh, 'P', degree)
    bcs = [DirichletBC(V, u_D, bc) for bc in bc_funs]
    u = TrialFunction(V)
    v = TestFunction(V)
    FF = dot(grad(u), grad(v))*dx - f*v*dx
    a = lhs(FF)
    L = rhs(FF)
    u = Function(V)
    solve(a == L, u, bcs)
    return u


def get_mesh(length, nx, ny, nz=None):
    """获得 mesh

    """
    if nz is None:
        mesh = RectangleMesh(Point(0.0, 0.0), Point(length, length), nx, ny)
    else:
        mesh = BoxMesh(Point(0.0, 0.0, 0.0), Point(
            length, length, length), nx, ny, nz)
    return mesh


def get_mesh_grid(length, nx, ny, nz=None):
    """获取网格节点坐标
    """
    mesh = get_mesh(length, nx, ny, nz)
    if nz is None:
        xs = mesh.coordinates()[:, 0].reshape(nx + 1, nx + 1)
        ys = mesh.coordinates()[:, 1].reshape(nx + 1, ny + 1)
        return xs, ys, None
    xs = mesh.coordinates()[:, 0].reshape(nx + 1, ny + 1, nz + 1)
    ys = mesh.coordinates()[:, 1].reshape(nx + 1, ny + 1, nz + 1)
    zs = mesh.coordinates()[:, 2].reshape(nx + 1, ny + 1, nz + 1)
    return xs, ys, zs


def run_solver(ndim, length, length_unit, bcs, layout_list, u0,
               powers, nx, coordinates=False, is_plot=False, F=None, vtk=False):
    """求解器主函数.

    Args:
        ndim (int): 2 or 3, 问题维数
        length (float): board length
        length_unit (float): unit length
        bcs (list): bcs.    
        layout_list (list): unit 位置
        u0 (float): Dirichlet bc 上的值
        powers (list): 功率 list
        nx (int): x 方向上的单元数
        coordinates (bool, optional): 是否返回坐标矩阵. Defaults to False.
        is_plot (bool, optional): 是否画图. Defaults to False.
        F (ndarray, optional): 热源布局矩阵 F. Defaults to None.
        vtk (bool): 是否输出 vtk 文件.

    Returns:
        tuple: U, xs, ys, zs
    """
    ny = nx
    nz = nx if ndim == 3 else None
    u_D = Constant(u0)
    if len(bcs) > 0:
        if ndim == 2:
            bc_funs = [LineBoundary(line).get_boundary() for line in bcs]
        else:
            bc_funs = [RecBoundary(rec).get_boundary() for rec in bcs]
    else:
        bc_funs = [lambda x, on_boundary:on_boundary]  # 边界都为 Dirichlet

    if F is None:
        f = Source(layout_list, length, length_unit, powers)
    else:
        f = SourceF(F, length)
    u = solver(f, u_D, bc_funs, ndim, length, nx, ny, nz)
    if is_plot:
        import matplotlib.pyplot as plt
        plt.plot(u)
    if vtk:
        vtkfile = File('solution.pvd')
        vtkfile << u
    if ndim == 2:
        U = u.compute_vertex_values().reshape(nx + 1, nx + 1)
    else:
        U = u.compute_vertex_values().reshape(nx + 1, nx + 1, nx + 1)
    if coordinates:
        xs, ys, zs = get_mesh_grid(length, nx, ny, nz)
    else:
        xs, ys, zs = None, None, None
    return U, xs, ys, zs

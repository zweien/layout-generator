# -*- encoding: utf-8 -*-
'''
@File    :   fenics_solver.py
@Time    :   2020/03/13 00:43:50
@Author  :   Zweien
@Contact :   278954153@qq.com
@Desc    :   Fenics solver.
'''

import numpy as np
from fenics import *

set_log_level(40) # ERROR = 40
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
        for i, (l, power) in enumerate(zip(self.layout_list, self.powers)):
            lx, ly = l % self.n, l // self.n
            if (self.length_unit * lx <= x[0] <= self.length_unit * (lx + 1)) \
                    and (self.length_unit * ly <= x[1] <= self.length_unit * (ly + 1)):
                return power
        else:
            return 0 

    def value_shape(self):
        return ()

class SourceF(UserExpression):
    """热源, 矩阵表达"""
    def __init__(self, F, length):
        """
        
        Arguments:
            F {2D array} -- 组件节点矩阵
            length {float} -- 布局板尺寸
            length_unit {float} -- 组件尺寸
        """
        super().__init__(self)
        self.F = F
        self.length = length

    def eval(self, value, x):
        value[0] = self.get_source(x)

    def get_source(self, x):
        assert self.F.ndim == 2
        m, n = self.F.shape
        col = int(x[0] / self.length * (n - 1))
        row = int(x[1] / self.length * (m - 1))
        return self.F[row, col]

    def value_shape(self):
        return ()



class LineBoundary():
    """线段边界
    """
    def __init__(self, line):
        """
        
        Arguments:
            line {list} -- 表示边界的线段，格式为 [[起点x, 起点y], [终点x, 终点y]]
        """
        self.line = line
        assert len(line) == 2, "线段包含两个点"
        assert len(line[0]) == 2  and len(line[1]) == 2, "二维点"

    def get_boundary(self):
        """构造 fenics 所需 bc 函数
        
        Returns:
            function -- fenics 所需 bc
        """
        def boundary(x, on_boundary):
            if on_boundary:
                (lx, ly), (rx, ry) = self.line
                if (lx - TOL <= x[0] <= rx + TOL) and (ly - TOL <= x[1] <= ry + TOL):
                    return True
            return False
        return boundary


def solver(f, u_D, bc_funs, length, nx, ny, degree=1):
    """有限元求解器
    
    Arguments:
        f {fenics.Expression} -- heat source
        u_D {fenics.Expression} -- Dirichlet bc function
        bc_funs {list} -- bcs
        nx {int} -- x 方向网格数
        ny {int} -- y 方向网格数
    
    Keyword Arguments:
        degree {int} -- 有限元 degree (default: {1})
    
    Returns:
        fenics.Function -- fenics 解函数
    """
    mesh = RectangleMesh(Point(0.0, 0.0), Point(length, length), nx, ny)
    V = FunctionSpace(mesh, 'P', 1)
    bcs = [DirichletBC(V, u_D, bc) for bc in bc_funs] 
    u = TrialFunction(V)
    v = TestFunction(V)   
    FF = dot(grad(u), grad(v))*dx - f*v*dx
    a = lhs(FF)
    L = rhs(FF)
    u = Function(V)
    solve(a == L, u, bcs)
    return u
    

def get_mesh_grid(length, nx, ny):
    """获取网格节点坐标
    """
    mesh = RectangleMesh(Point(0.0, 0.0), Point(length, length), nx, ny)
    xs = mesh.coordinates()[:, 0].reshape(ny + 1, nx + 1)
    ys = mesh.coordinates()[:, 1].reshape(ny + 1, nx + 1)
    return xs, ys


def run_solver(length, length_unit, lines_D, layout_list, u0,
                powers, nx, ny, coordinates=False, is_plot=False, F=None):
    """求解器
    """

    u_D = Constant(u0)
    if len(lines_D) > 0:
        bc_funs = [LineBoundary(line).get_boundary() for line in lines_D]
    else:
        bc_funs = [lambda x, on_boundary: on_boundary]
    if F is None:
        f = Source(layout_list, length, length_unit, powers)
    else:
        f = SourceF(F, length)
    u = solver(f, u_D, bc_funs, length, nx, ny)
    if is_plot:
        plt.plot(u)
    U = u.compute_vertex_values().reshape(ny + 1, nx + 1)
    if not coordinates:
        return U
    else:
        xs, ys = get_mesh_grid(length, nx, ny)
        return U, xs, ys
    return U

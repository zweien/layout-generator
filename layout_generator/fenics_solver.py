'''
fenics solver
'''
import numpy as np
from fenics import *

 
class Source(UserExpression):
    """热源布局"""
    def __init__(self, layout_list, length, length_unit):
        """
        
        Arguments:
            layout_list {list} -- 组件摆放位置
            length {float} -- 布局板尺寸
            length_unit {float} -- 组件尺寸
        """
        super().__init__(self)
        self.layout_list = layout_list
        self.length = length
        self.length_unit = length_unit
        self.n = length / length_unit  # unit_per_row

    def eval(self, value, x):
        value[0] = power * self.get_source(x)

    def get_source(self, x):
        for l in self.layout_list:
            lx, ly = l % self.n, l // self.n
            if (self.length_unit * lx <=x[0]<= self.length_unit * (lx+1)) \
                and (self.length_unit * ly <=x[1]<= self.length_unit * (ly+1)):
                return 1
        else:
            return 0 

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
                if (lx <= x[0] <= rx) and (ly <= x[1] <= ry): return True
            return False
        return boundary


def solver(f, u_D, bc_funs, nx, ny, degree=1):
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


def run_solver(length, length_unit, lines_D, layout_list, u0,
                power, nx, ny, is_plot=False):
    
    u_D = Constant(u0)
    bc_funs = [LineBoundary(line).get_boundary() for line in lines_D]
    f = Source(layout_list, length, length_unit)
    u = solver(f, u_D, bc_funs, nx, ny)
    if is_plot: plot(u)
    U = u.compute_vertex_values().reshape(nx+1, ny+1)
    return U


if __name__ == "__main__":
    # test
    length = 0.1
    unit_per_row = 10
    length_unit = length / unit_per_row
    power = 1e4
    u0 = 298.
    lines_D = [[[0.01, 0], [0.02, 0]], [[0.08, 0], [0.09, 0]]]
    layout_list = [25]

    run_solver(length, length_unit, lines_D, layout_list, u0, power, 20, 20, True)
    

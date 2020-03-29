# -*- encoding: utf-8 -*-
'''
Desc      :   config based argparser.
'''
# File    :   configarg.py
# Time    :   2020/03/29 15:17:56
# Author  :   Zweien
# Contact :   278954153@qq.com


import configargparse
import sys
import os

here = os.path.abspath(os.path.dirname(__file__))


def bc_convert(parm: str) -> list:
    """将 yml 中 bcs 转换为 list
    """
    s = parm.replace('"', '').replace("'", '')  # del outside "
    return eval(s)


default_conf = os.path.join(here, 'default.yml')

parser = configargparse.ArgParser(default_config_files=[default_conf],
                                  description='Generate layout dataset.')
parser.add('--config', is_config_file=True, help='config file path')
parser.add('--test', action='store_true', help='test mode')
parser.add('--length', type=float, help='board length')
parser.add('--length_unit', type=float, help='unit length')
parser.add('--bcs', type=bc_convert,
           help='Dirichlet boundarys, use two points to represent a line segment')
parser.add('--power', action='append', type=float,
           help='possible power of each unit')
parser.add('--data_dir', type=str, help='dir to store generated layout data')
parser.add('--sampler', type=str, choices=['uniform'], help='sampler method')
parser.add('--fem_degree', type=int, help='fem degree in fenics')
parser.add('--u_D', type=int, help='value on Dirichlet boundary')
parser.add('--unit_n', type=int, help='number of units')
parser.add('--nx', type=int, help='number of grid in x direction')
# parser.add('--ny', type=int, help='number of grid in y direction')
# parser.add('--nz', type=int, help='number of grid in z direction')
parser.add('--sample_n', type=int, help='number of samples')
parser.add('--seed', type=int, help='seed in np.random module')
parser.add('--file_format', type=str,
           choices=['mat'], help='dataset file format')
parser.add('--prefix', type=str, help='prefix of file')
parser.add('--method', type=str,
           choices=['fenics', ], help='method to solve the equation')
parser.add('--worker', type=int, help='number of workers')
parser.add('--ndim', type=int, choices=[2, 3], help='dimension')
parser.add('--vtk', action='store_true', default=False, help='output vtk file')

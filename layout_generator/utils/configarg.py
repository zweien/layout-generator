import configargparse
import sys, os


def bc_convert(parm):
    """将 yml 中 bcs 转换为 list
    """
    s = ' '.join(parm).strip("'").replace(' ', '')
    return eval(s)[0]


parser = configargparse.ArgParser()

parser.add('--config', is_config_file=True, help='config file path')
parser.add('--length', type=float, help='board length')
parser.add('--length_unit', type=float, help='unit length')
parser.add('--bcs', action='append', type=bc_convert, help='Dirichlet boundarys, use tow point to represent a line segment')
parser.add('--power', type=float, help='power of each unit')
parser.add('--data_dir', type=str, help='dir to store generated layout data')
parser.add('--sampler', type=str, choices=['uniform'], help='sampler method')
parser.add('--fem_degree', type=int, help='fem degree in fenics')
parser.add('--u_D', type=int, help='value on Dirichlet boundary')
parser.add('--unit_n', type=int, help='number of units')
parser.add('--nx', type=int, help='number of grid in x direction')
parser.add('--ny', type=int, help='number of grid in y direction')
parser.add('--sample_n', type=int, help='number of samples')
parser.add('--seed', type=int, help='seed in np.random module')
parser.add('--file_format', type=str, choices=['mat'], help='dataset file format')
parser.add('--prefix', type=str, help='prefix of file')
parser.add('--method', type=str, choices=['fenics', 'fenics_additive'], help='method to solve the equation')

options = parser.parse_args()

print(parser.format_values())

if options.data_dir is not None:
    if not os.path.isdir(options.data_dir):
        os.mkdir(options.data_dir)
    config_file_data = options.data_dir + '/config.yml'
    parser.write_config_file(options, [config_file_data])

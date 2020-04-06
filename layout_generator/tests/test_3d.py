import pytest
from pathlib import Path
import argparse
import numpy as np
from layout_generator.utils import get_parser
from layout_generator.utils import io
from layout_generator.generator import generate_from_cli
from layout_generator.utils import __file__ as utils__file__

def test_3d_generator(tmp_path):
    config_path = Path(utils__file__).parent / 'default3D.yml'
    assert config_path.exists(), 'default3D.yml does not exist'
    parser = get_parser(config_path)
    options, _ = parser.parse_known_args()
    options.data_dir = tmp_path
    options.bcs = []
    options.sample_n = 2
    options.worker = 2
    # assert options == 1
    generate_from_cli(options)

    data_dir = Path(options.data_dir)

    data_path_list = list(data_dir.glob(f'*.{options.file_format}'))
    assert data_dir.exists()
    assert len(data_path_list) == options.sample_n

    datum_path = data_path_list[0]

    r = io.load_mat(datum_path)
    assert set(['u', 'F', 'list', 'xs', 'ys', 'zs']).issubset(set(r.keys()))
    F = r['F']
    u = r['u']
    assert u.shape == (options.nx + 1, ) * options.ndim
    assert F.max() == options.power[0]
    assert u.min() >= options.u_D


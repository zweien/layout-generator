import pytest
import argparse
import numpy as np
from layout_generator.utils.configarg import parser
from layout_generator.utils import io

def test_save(tmp_path):
    options = parser.parse_args('')
    options.data_dir = tmp_path
    i = 1; U = [[1, 2]]; xs = [1]; ys= [2]; layout_pos_list=[1,2]
    io.save(options, i, U, xs, ys, layout_pos_list)

    data = io.loadmat(tmp_path / f'{options.prefix}{i}.{options.file_format}')
    assert data['u'] == pytest.approx(np.array(U))
import pytest
from configargparse import ArgumentParser
import numpy as np
from layout_generator.utils.configarg import get_parser_discrete
from layout_generator.utils import io


def test_save(tmp_path):
    parser = ArgumentParser()
    parser = get_parser_discrete(parser)
    options = parser.parse_args("")
    options.data_dir = tmp_path
    i = 1
    U = [[1, 2]]
    xs = [1]
    ys = [2]
    F = [[1]]
    layout_pos_list = [1, 2]
    io.save(options, i, U, xs, ys, F, layout_pos_list)
    # assert tmp_path == 1
    data = io.load_mat(tmp_path / f"{options.prefix}{i}.{options.file_format}")
    assert data["u"] == pytest.approx(np.array(U))

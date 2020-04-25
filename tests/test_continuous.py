import pytest
import numpy as np

from layout_generator.sampler import continuous
from layout_generator.utils.configarg_c import get_parser


# 测试 size_board 与 grid_board
@pytest.mark.parametrize("size_board", [0.1])
@pytest.mark.parametrize("grid_board", [100, 200])
def test_c(size_board, grid_board):
    parser = get_parser()
    options, _ = parser.parse_known_args()
    num = len(options.units)
    task = continuous.get_task(
        geometry_board="s",
        size_board=size_board,
        grid_board=grid_board,
        geometry=["r"] * num,
        size=options.units,
        angle=options.angles,
        intensity=options.powers,
        rad=False,
    )
    F, _ = task.sample_layout_seq()
    assert F.shape == (grid_board, grid_board)

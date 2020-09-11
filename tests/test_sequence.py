import pytest
from layout_generator.sampler.continuous import get_task
from layout_generator.sampler.continuous.config import (
    angle,
    intensity,
    size,
    geometry,
)


# 测试 size_board 与 grid_board
@pytest.mark.parametrize("size_board", [0.1])
@pytest.mark.parametrize("grid_board", [100, 200])
def test_size_grid_board(size_board, grid_board):

    task = get_task(
        geometry_board="s",
        size_board=size_board,
        grid_board=grid_board,
        geometry=geometry,
        size=size,
        angle=angle,
        intensity=intensity,
        method="sequence",
    )
    F, _ = task.sample_until_success()
    assert F.shape == (grid_board, grid_board)

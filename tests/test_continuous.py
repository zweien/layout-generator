import sys
import pytest
from layout_generator.sampler.continuous import get_task

# from layout_generator.sampler.continuous.config import (
#     angle,
#     intensity,
#     size,
#     geometry,
# )
from layout_generator.cli import main


@pytest.fixture(scope="module")
def config():
    sys.argv = ["layout_generator", "generate_c"]
    parser, options = main(debug=True)
    return parser, options


# 测试 size_board 与 grid_board
@pytest.mark.parametrize("size_board", [0.1, 0.2])
@pytest.mark.parametrize("grid_board", [20, 100, 150, 200, 201])
def test_size_grid_board_gibbs(config, size_board, grid_board):
    parser, options = config
    task = get_task(
        geometry_board="s",
        size_board=size_board,
        grid_board=grid_board,
        geometry=["r"] * len(options.units),
        size=options.units,
        angle=options.angles,
        intensity=options.powers,
        method="gibbs",
        rad=False,
    )
    task.warmup()
    F, _ = task.sample_until_success()
    assert F.shape == (grid_board, grid_board)


# 测试 size_board 与 grid_board
@pytest.mark.parametrize("size_board", [0.1])
@pytest.mark.parametrize("grid_board", [100, 200])
def test_size_grid_board_sequence(config, size_board, grid_board):
    parser, options = config
    task = get_task(
        geometry_board="s",
        size_board=size_board,
        grid_board=grid_board,
        geometry=["r"] * len(options.units),
        size=options.units,
        angle=options.angles,
        intensity=options.powers,
        method="sequence",
        rad=False,
    )
    F, _ = task.sample_until_success()
    assert F.shape == (grid_board, grid_board)


class TestTask:
    @pytest.fixture(scope="class")
    def task(self, config):
        parser, options = config
        _task = get_task(
            geometry_board="s",
            size_board=options.length,
            grid_board=options.nx,
            geometry=["r"] * len(options.units),
            size=options.units,
            angle=options.angles,
            intensity=options.powers,
            method=None,
            rad=False,
        )
        return _task

    def test_layout_from_pos(self, task):
        pos = [None] * len(task.components)
        pos[0] = (0.0, 0.0)
        layout = task.layout_from_pos(pos)
        grid = task.domain.grid
        assert layout.shape == (grid, grid)

    def test_is_overlaping(self, task):
        pos = [None] * len(task.components)
        pos[0] = (0.0, 0.0)
        assert task.is_overlaping(pos) is False

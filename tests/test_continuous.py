import sys
import pytest
from layout_generator.sampler.continuous import get_task
from layout_generator.generator_c import layout_pos2temp
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

    @pytest.fixture(scope="class")
    def pos(self, config):
        parser, options = config
        _task = get_task(
            geometry_board="s",
            size_board=options.length,
            grid_board=options.nx,
            geometry=["r"] * len(options.units),
            size=options.units,
            angle=options.angles,
            intensity=options.powers,
            method="gibbs",
            rad=False,
        )
        _task.warmup(initial_position=None, burn_in_period=1)
        return _task.sample_location()

    @pytest.fixture(scope="class")
    def powers(self, task):
        pows = [10000] * len(task.components)
        pows[1] = 20000
        return pows

    def test_layout_from_pos(self, task, pos, powers):
        layout = task.layout_from_pos(pos, powers)
        grid = task.domain.grid
        assert layout.shape == (grid, grid)

        pos = [(0.0, 0.0)] * len(pos)
        powers = [10000] * len(pos)
        layout = task.layout_from_pos(pos, powers)
        grid = task.domain.grid
        assert layout.shape == (grid, grid)

    def test_is_overlaping(self, pos, task):
        assert task.is_overlaping(pos) is False

        pos = [(0.0, 0.0)] * len(pos)
        assert task.is_overlaping(pos) is True

    def test_layout_pos2temp(self, task, config, pos, powers):
        parser, options = config
        layout, temp = layout_pos2temp(options, pos, powers)

        assert layout.shape == (task.domain.grid,) * options.ndim
        assert temp.min() >= 298
        assert all(power in layout for power in powers)

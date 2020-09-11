import sys
from layout_generator.cli import main
import layout_generator.sampler.continuous as continuous


def test_multi_powers_seq():
    sys.argv = "layout_generator generate_c".split()
    parser, options = main(debug=True)

    # powers is 2D list
    assert isinstance(options.powers, list)
    assert isinstance(options.powers[0], list)

    n = len(options.powers)
    options.powers[0] = [1000, 2000]
    task: continuous.sequence_layout_sampling.TaskSeq = continuous.get_task(
        geometry_board="s",
        size_board=options.length,
        grid_board=options.nx,
        geometry=["r"] * n,
        size=options.units,
        angle=options.angles,
        intensity=options.powers,
        rad=False,
        method="sequence",
    )

    # 每个组件的功率都是 list
    assert (isinstance(p, list) for p in task.components.intensity)

    task.warmup()
    layout, _ = task.sample_until_success()
    assert layout.shape == (options.nx,) * 2
    assert any(p in layout for p in options.powers[0])


def test_multi_powers_gibbs():
    sys.argv = "layout_generator generate_c".split()
    parser, options = main(debug=True)

    n = len(options.powers)
    options.powers[0] = [1000, 2000]
    task: continuous.sequence_layout_sampling.TaskSeq = continuous.get_task(
        geometry_board="s",
        size_board=options.length,
        grid_board=options.nx,
        geometry=["r"] * n,
        size=options.units,
        angle=options.angles,
        intensity=options.powers,
        rad=False,
        method="gibbs",
    )

    task.warmup()
    layout, _ = task.sample_until_success()
    assert layout.shape == (options.nx,) * 2
    assert any(p in layout for p in options.powers[0])

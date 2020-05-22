import pytest
import sys
import numpy as np
from layout_generator.sampler.continuous import (
    sequence_layout_sampling,
    gibbs_layout_sampling,
)
from layout_generator.cli import main
import layout_generator.sampler.continuous as continuous
# from layout_generator.sampler.continuous.config import intensity, angle, size


def test_mulit_powers_seq():
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

    task.warmup()
    layout, _ = task.sample()
    assert layout.shape == (options.nx,) * 2
    assert any(p in layout for p in options.powers[0])


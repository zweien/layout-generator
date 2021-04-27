import sys
import numpy as np
from layout_generator.cli import main
from layout_generator.sampler import continuous
from layout_generator.fenics_solver import run_solver_c
from layout_generator.generator_c_power import observe_temperature_of_points


def test_powers():
    sys.argv = "layout_generator generate_c_power".split()
    parser, options = main(debug=True)

    # powers is 2D list
    assert isinstance(options.powers, list)
    assert isinstance(options.powers[0], list)

    positions = np.array([k for k in options.positions])
    if options.positions_type == "coord":
        pass
    elif options.positions_type == "grid":
        positions = positions / (options.nx + 1) * options.length
    else:
        raise LookupError(f"Type {options.positions_type} is not supported!")

    task = continuous.get_task_powers_sampling(
        geometry_board="s",
        size_board=options.length,
        grid_board=options.nx,
        geometry=["r"] * len(options.units),
        size=options.units,
        angle=options.angles,
        intensity=options.powers,
        rad=False,
        position=positions,
    )

    # 每个组件的功率都是 list
    assert (isinstance(p, list) for p in task.components.intensity)

    task.warmup()
    layout, _ = task.sample_until_success()
    assert layout.shape == (options.nx,) * 2
    # assert any(p in layout for p in options.powers[0])


def test_interpolation():
    sys.argv = "layout_generator generate_c_power".split()
    parser, options = main(debug=True)

    positions = np.array([k for k in options.positions])
    if options.positions_type == "coord":
        pass
    elif options.positions_type == "grid":
        positions = positions / (options.nx + 1) * options.length
    else:
        raise LookupError(f"Type {options.positions_type} is not supported!")

    task = continuous.get_task_powers_sampling(
        geometry_board="s",
        size_board=options.length,
        grid_board=options.nx,
        geometry=["r"] * len(options.units),
        size=options.units,
        angle=options.angles,
        intensity=options.powers,
        rad=False,
        position=positions,
    )

    task.warmup()
    F, _ = task.sample_until_success()
    intensity = task.intensity_sample

    if options.bcs is None:
        options.bcs = []

    U, xs, ys, zs = run_solver_c(
        options.ndim,
        options.length,
        options.units,
        options.bcs,
        options.u_D,
        intensity,
        options.nx,
        F,
        coordinates=True,
    )

    ind_x = np.array([10, 20, 40, 60, 80, 100])
    ind_y = np.array([100, 80, 60, 40, 20, 10])
    points_x = xs[ind_x, ind_y]
    points_y = ys[ind_x, ind_y]
    points_realvalue = U[ind_x, ind_y].reshape(-1, 1)

    # points = np.array(options.observation_points)
    points = np.hstack((points_x.reshape(-1, 1), points_y.reshape(-1, 1)))
    temp_points = observe_temperature_of_points(points, xs, ys, U).reshape(
        -1, 1
    )

    assert len(temp_points) == len(points)
    assert np.sum(np.abs(points_realvalue - temp_points)) < 1e-10

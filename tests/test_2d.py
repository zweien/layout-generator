import sys
import argparse
from layout_generator.utils import io
from layout_generator.cli import main
from layout_generator.generator import layout_pos_list2temp


def test_2d_generator(tmp_path, capsys):
    try:
        from pytest_cov.embed import cleanup_on_sigterm
    except ImportError:
        pass
    else:
        cleanup_on_sigterm()
    sample_n = 10
    worker = 4
    path = tmp_path / "test"
    sys.argv = [
        "layout_generator",
        "generate",
        "--data_dir",
        str(path),
        "--bcs",
        "[]",
        "--sample_n",
        str(sample_n),
        "--worker",
        str(worker),
    ]
    # parser = get_parser()
    # options, _ = parser.parse_known_args()

    options = main(options_flag=True)

    data_dir = path
    # assert data_dir == 's'
    # data_path_list = os.listdir(options.data_dir)
    data_path_list = list(data_dir.glob(f"*.{options.file_format}"))
    assert data_dir.exists()
    assert len(data_path_list) == options.sample_n
    datum_path = data_path_list[0]

    r = io.load_mat(datum_path)
    assert set(["u", "F", "list", "xs", "ys"]).issubset(set(r.keys()))
    u = r["u"]
    assert u.shape == (options.nx,) * options.ndim
    assert u.min() >= options.u_D

    # plot dir
    sys.argv = [
        "layout_generator",
        "plot",
        "-p",
        str(path),
        "--dir",
        "--worker",
        "2",
    ]
    main()
    assert len(list(path.glob("*.png"))) == options.sample_n

    sys.argv = [
        "layout_generator",
        "plot",
        "-p",
        str(path),
        "--worker",
        "2",
        "-o",
        str(path / "sub"),
    ]
    main()
    outpath = path / "sub"
    assert len(list(outpath.glob("*.png"))) == options.sample_n

    # plot single file
    file_path = next(path.glob("*.mat"))
    sys.argv = [
        "layout_generator",
        "plot",
        "-p",
        str(file_path),
        "-o",
        str(path / "o.png"),
        "--worker",
        "2",
    ]
    options = main(options_flag=True)
    png_path = path / "o.png"
    assert png_path.exists()


def test_2d_bc(tmp_path):
    try:
        from pytest_cov.embed import cleanup_on_sigterm
    except ImportError:
        pass
    else:
        cleanup_on_sigterm()
    sample_n = 10
    worker = 4
    path = tmp_path / "test"
    sys.argv = [
        "layout_generator",
        "generate",
        "--data_dir",
        str(path),
        "--bcs",
        "[[0.01, 0], [0.02, 0]]",
        "--bcs",
        "[[0.08, 0], [0.09, 0]]",
        "--sample_n",
        str(sample_n),
        "--worker",
        str(worker),
    ]
    options = main(options_flag=True)
    data_dir = path
    # assert data_dir == 's'
    # data_path_list = os.listdir(options.data_dir)
    data_path_list = list(data_dir.glob(f"*.{options.file_format}"))
    assert data_dir.exists()
    assert len(data_path_list) == options.sample_n
    datum_path = data_path_list[0]

    r = io.load_mat(datum_path)
    assert set(["u", "F", "list", "xs", "ys"]).issubset(set(r.keys()))
    u = r["u"]
    assert u.shape == (options.nx,) * options.ndim
    assert u.min() >= options.u_D


def test_layout_pos_list2temp():
    options = argparse.Namespace(
        ndim=2,
        length=0.1,
        length_unit=0.01,
        unit_per_row=10,
        bcs=[[[0.05, 0], [0.07, 0]]],
        u_D=298,
        nx=199,
    )
    powers = [8000, 2000]
    layout_pos_list = [15, 55]
    F, U, xs, ys, zs = layout_pos_list2temp(options, layout_pos_list, powers)
    assert U.shape == (200, 200)
    assert U.min() >= 298
    assert all(power in F for power in powers)

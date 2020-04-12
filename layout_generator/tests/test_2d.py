import sys
from layout_generator.utils import get_parser
from layout_generator.utils import io
from layout_generator.utils import visualize
from layout_generator.cli import main


def test_2d_generator(tmp_path, capsys):
    sample_n = 10
    worker = 2
    path = tmp_path / "test"
    sys.argv = [
        "layout_generator",
        "--data_dir",
        str(path),
        "--bcs",
        "[]",
        "--sample_n",
        str(sample_n),
        "--worker",
        str(worker),
    ]
    parser = get_parser()
    options, _ = parser.parse_known_args()

    main()
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
    sys.argv = ["layout_plot", "-p", str(path), "--dir", "--worker", "2"]
    visualize.main()
    assert len(list(path.glob("*.png"))) == options.sample_n

    # plot single file
    file_path = next(path.glob("*.mat"))
    sys.argv = [
        "layout_plot",
        "-p", str(file_path),
        "-o", str(path / "o.png"),
        "--worker", "2"
    ]
    visualize.main()
    png_path = path / "o.png"
    assert png_path.exists()

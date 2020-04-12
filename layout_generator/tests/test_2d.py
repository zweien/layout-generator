import sys
from pathlib import Path
from layout_generator.utils import get_parser
from layout_generator.utils import io
from layout_generator.utils import visualize
from layout_generator.cli import main


def test_2d_generator(tmp_path, capsys):
    sample_n = 10
    worker = 2
    sys.argv = [
        "layout_generator",
        "--data_dir", str(tmp_path),
        "--bcs", "[]",
        "--sample_n", str(sample_n),
        "--worker", str(worker)
    ]
    parser = get_parser()
    options, _ = parser.parse_known_args()

    main()

    data_dir = Path(options.data_dir)
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

    # generator_plot
    parser_plot = visualize.get_parser()
    args_plot, _ = parser_plot.parse_known_args()
    args_plot.path = options.data_dir
    args_plot.dir = True
    args_plot.worker = 2
    visualize.plot_dir(
        args_plot.path, out=args_plot.output, worker=args_plot.worker
    )
    assert len(list(Path(args_plot.path).glob("*.png"))) == options.sample_n

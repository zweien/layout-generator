import pytest
from pathlib import Path
import sys
from layout_generator.utils.configarg import get_parser_discrete
from layout_generator.utils import io
from layout_generator.generator import generate_from_cli
from layout_generator.utils import __file__ as utils__file__
from layout_generator.cli import main


@pytest.fixture(scope="module")
def get_parser_options():
    config_path = Path(utils__file__).parent / "default3D.yml"
    assert config_path.exists(), "default3D.yml does not exist"

    sys.argv = [
        "layout_generator",
        "generate",
        "--config",
        str(config_path),
        "--sample_n",
        "2",
        "--worker",
        "2",
    ]
    parser, options = main(debug=True)
    return parser, options


def test_3d_generator(get_parser_options, tmp_path):

    _, options = get_parser_options
    options.data_dir = str(tmp_path)
    generate_from_cli(options)

    data_dir = Path(options.data_dir)

    data_path_list = list(data_dir.glob(f"*.{options.file_format}"))
    assert data_dir.exists()
    assert len(data_path_list) == options.sample_n

    datum_path = data_path_list[0]

    r = io.load_mat(datum_path)
    assert set(["u", "F", "list", "xs", "ys", "zs"]).issubset(set(r.keys()))
    F = r["F"]
    u = r["u"]
    assert u.shape == (options.nx + 1,) * options.ndim
    assert F.max() == options.power[0]
    assert u.min() >= options.u_D


def test_3d_bc(tmp_path, get_parser_options):

    _, options = get_parser_options
    options.data_dir = tmp_path
    options.bcs = [[[0, 0.05, 0.05], [0, 0.07, 0.07]]]
    options.sample_n = 1
    options.worker = 1
    # assert options == 1
    generate_from_cli(options)

    data_dir = Path(options.data_dir)

    data_path_list = list(data_dir.glob(f"*.{options.file_format}"))
    assert data_dir.exists()
    assert len(data_path_list) == options.sample_n

    datum_path = data_path_list[0]

    r = io.load_mat(datum_path)
    assert set(["u", "F", "list", "xs", "ys", "zs"]).issubset(set(r.keys()))
    F = r["F"]
    u = r["u"]
    assert u.shape == (options.nx + 1,) * options.ndim
    assert F.max() == options.power[0]
    assert u.min() >= options.u_D

import pytest
import sys
from pathlib import Path
import numpy as np
import scipy.io as sio
from layout_generator.utils import convert, io


@pytest.fixture(scope="module")
def prepare_data_path(tmpdir_factory):
    tmpdir = tmpdir_factory.mktemp("data")
    num = 10
    shape = (200, 200)
    for i in range(num):
        u = np.random.randn(*shape)
        F = np.random.randn(*shape)
        lists = np.random.choice(100, 20)
        path = tmpdir / f"{i}.mat"
        sio.savemat(str(path), {"u": u, "F": F, "list": lists})

    return Path(tmpdir)


def test_get_mat_shape(prepare_data_path):
    path = prepare_data_path
    fns = list(path.glob("*.mat"))
    fn = fns[0]
    mat_shape = convert.get_mat_shape(fn)
    assert mat_shape["u"] == (200, 200)


def test_mat2h5(prepare_data_path: Path):
    path = prepare_data_path
    h5_path: Path = path / "h5.h5"
    convert.mat2h5(path, h5_path)
    assert h5_path.exists()
    ds = io.load_h5(h5_path)
    assert ds["u"].shape == (10, 200, 200)
    assert ds["F"].shape == (10, 200, 200)
    assert ds["list"].shape == (10, 1, 20)


def test_cli(prepare_data_path: Path, bash):

    path = prepare_data_path
    h5_path: Path = path / "h5.h5"
    # bash.run_script("layout_convert", ["-i", path, "-o", h5_path, "worker", '1'])
    sys.argv = [
        "layout_convert",
        "-i",
        str(path),
        "-o",
        str(h5_path),
        "--worker",
        "1",
    ]
    convert.main()

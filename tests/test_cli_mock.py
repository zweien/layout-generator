import sys
import pytest
from layout_generator.cli import main
from layout_generator.about import __package_name__, __version__


def test_cli_mock(capsys):
    sys.argv = ["layout_generator", "-V"]
    with pytest.raises(SystemExit):
        main()
    captured = capsys.readouterr()
    assert captured.out == f"{__package_name__} version: {__version__}\n"

    sys.argv = ["layout_generator", "generate", "--test"]
    with pytest.raises(SystemExit):
        main()


def test_shell(bash):
    version = bash.run_script('layout_generator', ['--version'])
    assert version == f"{__package_name__} version: {__version__}"

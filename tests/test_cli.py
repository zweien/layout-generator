import pytest
import sys
import argparse
from layout_generator.cli import main


def test_cli_default():
    # default config test
    sys.argv = ["layout_generator", "generate"]
    parser, options = main(debug=True)
    assert options.length == 0.1
    assert options.prefix == "Example"
    # assert options.bcs == [ [[0.01, 0], [0.02, 0]], [[0.08, 0], [0.09, 0]] ]
    # cli test
    bcs = parser.parse_args(
        [
            "generate",
            "--bcs",
            "[[0.25,0],[0.75,0]]",
            "--bcs",
            "[[0.1,0],[0.2,0]]",
        ]
    ).bcs
    assert bcs == [[[0.25, 0], [0.75, 0]], [[0.1, 0], [0.2, 0]]]
    # unknown method
    with pytest.raises(SystemExit), pytest.raises(argparse.ArgumentError):
        parser.parse_args("--method unknown")

    isinstance(options.power, list)
    power = parser.parse_args("generate --power 2 --power 3").power
    assert power == [2, 3]

    with pytest.raises(SystemExit):
        parser.parse_args("-V")

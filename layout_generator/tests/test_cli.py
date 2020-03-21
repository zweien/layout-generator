import pytest
import argparse
import numpy as np
from layout_generator.utils.configarg import parser
from layout_generator.utils import io


def test_cli_default():
    # default config test
    options = parser.parse_args('')
    assert options.length == 0.1
    assert options.prefix == 'Example'
    assert options.bcs == [ [[0.01, 0], [0.02, 0]], [[0.08, 0], [0.09, 0]] ]
    # cli test
    bcs = parser.parse_args(['--bcs', '"[[[0.25,0],[0.75,0]],[[0.1,0],[0.2,0]]]"']).bcs
    assert bcs == [[[0.25,0],[0.75,0]],[[0.1,0],[0.2,0]]]
    # unknown method
    with pytest.raises(SystemExit), pytest.raises(argparse.ArgumentError):
        parser.parse_args('--method unknown')

    assert options.power == [10000, 20000]

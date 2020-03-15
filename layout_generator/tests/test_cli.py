import pytest
from layout_generator.utils.configarg import parser

def test_cli_default():
    options = parser.parse_args()
    assert options.nx == 10
    assert options.bcs == [ [[0.01, 0], [0.02, 0]], [[0.08, 0], [0.09, 0]] ]
    bcs = parser.parse_args(['--bcs', '"[[[0.25,0],[0.75,0]],[[0.1,0],[0.2,0]]]"']).bcs
    assert bcs == [[[0.25,0],[0.75,0]],[[0.1,0],[0.2,0]]]



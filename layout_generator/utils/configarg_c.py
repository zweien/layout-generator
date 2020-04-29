# -*- encoding: utf-8 -*-
"""
Desc      :   config based argparser (continuous layout).
"""
# File    :   configarg_continuous.py
# Time    :   2020/04/22 18:34:23
# Author  :   Zweien
# Contact :   278954153@qq.com


import configargparse
import os
from pathlib import Path
import yaml
from ..about import __version__


def get_parser(config_path=None):
    if config_path is None:
        here = os.path.abspath(os.path.dirname(__file__))
        config_path = os.path.join(here, "default_c.yml")
    config_path = Path(config_path)
    assert config_path.exists(), "Config do not exist!"
    parser = configargparse.ArgParser(
        default_config_files=[str(config_path)],
        description="Generate layout dataset.",
        config_file_parser_class=configargparse.YAMLConfigFileParser,
    )
    parser.add("--config", is_config_file=True, help="config file path")
    parser.add("--test", action="store_true", help="test mode")
    parser.add("--length", type=float, help="board length")
    parser.add(
        "--bcs",
        type=yaml.safe_load,
        action="append",
        help="Dirichlet boundar",
    )
    parser.add(
        "--units",
        action="append",
        type=yaml.safe_load,
        help="shape of each unit",
    )
    parser.add(
        "--powers", action="append", type=float, help="power of each unit",
    )
    parser.add(
        "--angles", action="append", type=float, help="angle of each unit",
    )

    parser.add(
        "--data_dir", type=str, help="dir to store generated layout data"
    )
    parser.add(
        "--sampler",
        type=str,
        choices=["sequence", "gibbs"],
        help="sampler method",
    )
    parser.add("--fem_degree", type=int, help="fem degree in fenics")
    parser.add("--u_D", type=float, help="value on Dirichlet boundary")
    parser.add("--nx", type=int, help="number of grid in x direction")
    # parser.add('--ny', type=int, help='number of grid in y direction')
    # parser.add('--nz', type=int, help='number of grid in z direction')
    parser.add("--sample_n", type=int, help="number of samples")
    parser.add("--seed", type=int, help="seed in np.random module")
    parser.add(
        "--file_format", type=str, choices=["mat"], help="dataset file format"
    )
    parser.add("--prefix", type=str, help="prefix of file")
    parser.add(
        "--method",
        type=str,
        choices=["fenics"],
        help="method to solve the equation",
    )
    parser.add(
        "--worker", type=int, default=os.cpu_count(), help="number of workers"
    )
    parser.add("--ndim", type=int, choices=[2, 3], help="dimension")
    parser.add(
        "--vtk", action="store_true", default=False, help="output vtk file"
    )
    parser.add(
        "-V",
        "--version",
        action="version",
        version=f"layout-generator version: {__version__}",
    )
    return parser
# -*- encoding: utf-8 -*-
"""
Desc      :   config based argparser.
"""
# File    :   configarg.py
# Time    :   2020/03/29 15:17:56
# Author  :   Zweien
# Contact :   278954153@qq.com


import configargparse
import os
import shutil
from pathlib import Path
import yaml
import numpy as np
from ..about import __version__


here = Path(__file__).resolve().parent


def get_parser_common(parser: configargparse.ArgumentParser, config_name: str):
    config_path = here / config_name
    assert config_path.exists(), "Config do not exist!"

    parser._config_file_parser = configargparse.YAMLConfigFileParser()
    parser._default_config_files = [str(config_path)]

    parser.add("--config", is_config_file=True, help="config file path")
    parser.add("--test", action="store_true", help="test mode")
    parser.add("--length", type=float, help="board length")
    parser.add("--length_unit", type=float, help="unit length")
    parser.add(
        "--bcs",
        type=yaml.safe_load,
        action="append",
        help="Dirichlet boundaries",
    )

    parser.add(
        "--data_dir", type=str, help="dir to store generated layout data"
    )

    parser.add("--fem_degree", type=int, help="fem degree in fenics")
    parser.add("--u_D", type=int, help="value on Dirichlet boundary")
    parser.add("--nx", type=int, help="number of grid in x direction")
    # parser.add('--ny', type=int, help='number of grid in y direction')
    # parser.add('--nz', type=int, help='number of grid in z direction')
    parser.add("--sample_n", type=int, help="number of samples")
    parser.add(
        "--seed",
        type=int,
        default=np.random.randint(2 ** 32),
        help="seed in np.random module",
    )
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
    parser.add(
        "--task", help="task", choices=["discrete", "continuous"], type=str
    )
    return parser


def get_parser_discrete(
    parser: configargparse.ArgumentParser, config_path=None
):
    # parser = configargparse.ArgParser(
    #     default_config_files=[str(config_path)],
    #     description="Generate layout dataset.",
    #     config_file_parser_class=configargparse.YAMLConfigFileParser,
    # )
    parser = get_parser_common(parser, "default.yml")
    parser.add(
        "--power",
        action="append",
        type=float,
        help="possible power of each unit",
    )
    parser.add("--unit_n", type=int, help="number of units")
    parser.add(
        "--sampler", type=str, choices=["uniform"], help="sampler method"
    )

    return parser


def get_parser_continuous(
    parser: configargparse.ArgumentParser, config_path=None
):
    parser = get_parser_common(parser, "default_c.yml")
    parser.add(
        "--units",
        action="append",
        type=yaml.safe_load,
        help="shape of each unit",
    )
    parser.add(
        "--powers",
        action="append",
        type=yaml.safe_load,
        help="power of each unit",
    )
    parser.add(
        "--angles",
        action="append",
        type=float,
        help="angle of each unit",
    )

    parser.add(
        "--sampler",
        type=str,
        choices=["sequence", "gibbs"],
        help="sampler method",
    )

    return parser


def get_parser_continuous_power(
    parser: configargparse.ArgumentParser, config_path=None
):
    parser = get_parser_common(parser, "default_c_power.yml")
    parser.add(
        "--units",
        action="append",
        type=yaml.safe_load,
        help="shape of each unit",
    )
    parser.add(
        "--angles",
        action="append",
        type=float,
        help="angle of each unit",
    )
    parser.add(
        "--powers",
        action="append",
        type=yaml.safe_load,
        help="power of each unit",
    )
    parser.add(
        "--positions",
        action="append",
        type=yaml.safe_load,
        help="positions of each unit",
    )
    parser.add(
        "--positions_type",
        type=str,
        choices=['coord', 'grid'],
        help="the type of input positions: coord or grid",
    )
    parser.add(
        "--observation_points",
        action="append",
        type=yaml.safe_load,
        default=None,
        help="positions of chosen observation points",
    )
    parser.add(
        "--observation_points_type",
        type=str,
        choices=['coord', 'grid'],
        help="the type of observation points: coord or grid",
    )

    return parser


def get_parser_makeconfig(parser: configargparse.ArgumentParser):
    parser.add_argument(
        "--type",
        type=str,
        choices=["discrete2d", "discrete3d", "continuous2d"],
        help="config type",
    )
    parser.add_argument(
        "-o",
        "--output",
        type=str,
        default="template_config.yml",
        help="path for config template",
    )
    return parser


def makeconfig(options, output_path):
    config_file_dict = dict(
        discrete2d="default.yml",
        discrete3d="default3D.yml",
        continuous2d="default_c.yml",
    )
    config_name = config_file_dict[options.type]
    # config_path = os.path.join(here, config_name)
    config_path = Path(__file__).resolve().parent / config_name
    shutil.copyfile(config_path, output_path)
    print(f"Generated the config template in {output_path}")

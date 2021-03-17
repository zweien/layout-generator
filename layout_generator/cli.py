# -*- encoding: utf-8 -*-
"""
Desc      :   command line interface entry.
"""
# File    :   cli.py
# Time    :   2020/03/29 15:19:45
# Author  :   Zweien
# Contact :   278954153@qq.com


import os
from pathlib import Path
from configargparse import ArgumentParser
from .utils.configarg import (
    get_parser_discrete,
    get_parser_continuous,
    get_parser_continuous_power,
    get_parser_makeconfig,
    makeconfig,
)
from .utils.visualize import get_parser as get_plot_parser
from .utils.convert import get_parser as get_convert_parser
from .about import __version__


def handle_makeconfig(options):
    print(1)
    output_path = Path(options.output).resolve()
    makeconfig(options, output_path)


def handle_generate(options):
    from .generator import generate_from_cli

    preprocess(options.parser, options)
    generate_from_cli(options)
    options.nx += 1


def handle_generate_c(options):
    from .generator_c import generate_from_cli

    preprocess(options.parser, options)
    generate_from_cli(options)
    options.nx += 1


# newly added in 20210315
def handle_generate_c_power(options):
    from .generator_c_power import generate_from_cli

    preprocess(options.parser, options)
    generate_from_cli(options)
    options.nx += 1


def handle_plot(options):
    from .utils.visualize import plot_dir, plot_mat

    if not options.dir:
        plot_mat(
            options.path,
            plot=options.plot_off,
            save=options.output,
            worker=options.worker,
        )  # single file
    else:
        plot_dir(options.path, out=options.output, worker=options.worker)


def handle_convert(options):
    from .utils import convert

    convert_func = getattr(convert, options.mode)
    convert_func(options.input, options.output, worker=options.worker)


def preprocess(parser, options):
    if options.data_dir is not None:
        if not os.path.isdir(options.data_dir):
            os.mkdir(options.data_dir)
        # write config.yml in data_dir
        config_file_data = options.data_dir + "/config.yml"
        parser.write_config_file(options, [config_file_data])
        # cli 中 nx 为节点数，fenics求解过程中为单元数
        options.nx -= 1
        del_parser(options)  # fix error for multiprocessing


def del_parser(options):
    if hasattr(options, "parser"):
        del options.parser


def main(debug=False, options_flag=False):
    parser = ArgumentParser()
    parser.add(
        "-V",
        "--version",
        action="version",
        version=f"layout-generator version: {__version__}",
    )
    subparsers = parser.add_subparsers(title="commands")

    generate_parser = subparsers.add_parser(
        "generate", help="generate discrete layout data"
    )
    generate_parser = get_parser_discrete(generate_parser)
    generate_parser.set_defaults(
        handle=handle_generate, parser=generate_parser
    )

    generate_c_parser = subparsers.add_parser(
        "generate_c", help="generate continuous layout data"
    )
    generate_c_parser = get_parser_continuous(generate_c_parser)
    generate_c_parser.set_defaults(
        handle=handle_generate_c, parser=generate_c_parser
    )

    generate_c_power_parser = subparsers.add_parser(
        "generate_c_power",
        help="generate continuous layout data with sampling component powers",
    )
    generate_c_power_parser = get_parser_continuous_power(
        generate_c_power_parser
    )
    generate_c_power_parser.set_defaults(
        handle=handle_generate_c_power, parser=generate_c_power_parser
    )

    plot_parser = subparsers.add_parser("plot", help="plot layout data")
    plot_parser = get_plot_parser(plot_parser)
    plot_parser.set_defaults(handle=handle_plot)

    convert_parser = subparsers.add_parser(
        "convert", help="convert layout data"
    )
    convert_parser = get_convert_parser(convert_parser)
    convert_parser.set_defaults(handle=handle_convert)

    makeconfig_parser = subparsers.add_parser(
        "makeconfig", help="make template config"
    )
    makeconfig_parser = get_parser_makeconfig(makeconfig_parser)
    makeconfig_parser.set_defaults(handle=handle_makeconfig)

    options, _ = parser.parse_known_args()

    if hasattr(options, "test") and options.test:  # 仅测试，输出参数
        print(parser.format_values())
        print(options)
        # print(sys.argv)
        parser.exit()

    if debug:
        del_parser(options)
        return parser, options

    if hasattr(options, "handle"):
        options.handle(options)

    if options_flag:
        return options


if __name__ == "__main__":
    main()

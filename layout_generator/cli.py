# -*- encoding: utf-8 -*-
"""
Desc      :   command line interface entry.
"""
# File    :   cli.py
# Time    :   2020/03/29 15:19:45
# Author  :   Zweien
# Contact :   278954153@qq.com


import os
import sys
from layout_generator.utils import get_parser


def main():
    parser = get_parser()
    options = parser.parse_args()
    if options.test:  # 仅测试，输出参数
        print(parser.format_values())
        print(options)
        print(sys.argv)
    else:
        from .generator import generate_from_cli

        print(parser.format_values())
        if options.data_dir is not None:
            if not os.path.isdir(options.data_dir):
                os.mkdir(options.data_dir)
            # write config.yml in data_dir
            config_file_data = options.data_dir + "/config.yml"
            parser.write_config_file(options, [config_file_data])
        # cli 中 nx 为节点数，fenics求解过程中为单元数
        options.nx -= 1

        generate_from_cli(options)


if __name__ == "__main__":
    main()

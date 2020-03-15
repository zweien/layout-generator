# -*- encoding: utf-8 -*-
'''
@File    :   print_cli.py
@Time    :   2020/03/13 00:43:33
@Author  :   Zweien
@Contact :   278954153@qq.com
@Desc    :   CLI script entry point.
'''
import os
from .utils.configarg import parser


def main():
    options = parser.parse_args()
    if options.test:  # 仅测试，输出参数
        print(parser.format_values())
    else:
        from .generator import generate_from_cli
        if options.data_dir is not None:
            if not os.path.isdir(options.data_dir):
                os.mkdir(options.data_dir)
            # write config.yml in data_dir
            config_file_data = options.data_dir + '/config.yml'
            parser.write_config_file(options, [config_file_data])
        
        generate_from_cli(options)

if __name__ == "__main__":
    main()


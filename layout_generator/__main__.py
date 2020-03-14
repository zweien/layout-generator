# -*- encoding: utf-8 -*-
'''
@File    :   __main__.py
@Time    :   2020/03/13 00:42:11
@Author  :   Zweien
@Contact :   278954153@qq.com
@Desc    :   Generate layout dataset from command line interface.
             Example: python -m layout_generator --config config.yml
'''


# from layout_generator.generator import generate_from_cli
from layout_generator.print_cli import generate_from_cli

if __name__ == "__main__":
    generate_from_cli()

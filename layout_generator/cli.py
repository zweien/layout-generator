# -*- encoding: utf-8 -*-
'''
@File    :   print_cli.py
@Time    :   2020/03/13 00:43:33
@Author  :   Zweien
@Contact :   278954153@qq.com
@Desc    :   CLI script entry point.
'''

from layout_generator.utils.configarg import options

def main():
    if options.test:
        print(options)
    else:
        from .generator import generate_from_cli
        generate_from_cli()

if __name__ == "__main__":
    main()

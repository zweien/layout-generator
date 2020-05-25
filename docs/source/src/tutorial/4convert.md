# 数据转换脚本


## 简介

数据转换脚本 `layout_generator convert`，将生成的 mat 格式数据转换成其它格式

目前支持：
- [x] HDF5 单文件格式

## 用法

`$ layout_generator convert -h`
```text
usage: layout_generator convert [-h] -i INPUT -o OUTPUT [-m {mat2h5}]
                                [--worker WORKER] [--test]

optional arguments:
  -h, --help            show this help message and exit
  -i INPUT, --input INPUT
                        input dir path
  -o OUTPUT, --output OUTPUT
                        output path
  -m {mat2h5}, --mode {mat2h5}
                        converting mode
  --worker WORKER       number of workers
  --test                test mode
```

## 示例

1. 将 `example_data` 目录下 mat 数据转换为 HDF5 格式单文件，并保存为 `example.h5`
```
layout_generator convert -i example_data -o example.h5
```
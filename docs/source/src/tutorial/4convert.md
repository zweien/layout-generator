# 数据转换脚本


## 简介

数据转换脚本 `layout_convert`，将生成的 mat 格式数据转换成其它格式

目前支持：
- [x] HDF5 单文件格式

## 用法

`$ layout_convert -h`
```
usage: layout_convert [-h] -i INPUT -o OUTPUT [-m {mat2h5}] [--worker WORKER]

optional arguments:
  -h, --help            show this help message and exit
  -i INPUT, --input INPUT
                        input dir path
  -o OUTPUT, --output OUTPUT
                        output path
  -m {mat2h5}, --mode {mat2h5}
                        converting mode
  --worker WORKER       number of workers
```
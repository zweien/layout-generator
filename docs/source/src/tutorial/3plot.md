# 可视化脚本

可视化脚本 `layout_generator plot`，将生成数据转换为便于展示的图像

## 用法

- `layout_generator plot -h` 获取帮助
```
$ layout_plot -h

usage: layout_generator plot [-h] [-p PATH] [-o OUTPUT] [--plot-off] [--dir]
                             [--worker WORKER] [--test]

optional arguments:
  -h, --help            show this help message and exit
  -p PATH, --path PATH  file path
  -o OUTPUT, --output OUTPUT
                        output path
  --plot-off            turn off plot
  --dir                 path is dir
  --worker WORKER       number of workers
  --test                test mode
```

## 示例

可视化 `./data1` 目录下生成好的数据
 1. 转化单个数据文件`./data1/Example0.mat`，在相同目录下生成 png 文件, `layout_generator plot -p data1/Example0.mat --plot-off`
 1. 使用全部线程转化整个目下的文件，并将图片保存在相同目录，`layout_generator plot -p data1`，也可指定线程数量 `--worker`
     - 也可 `-o` 指定输出目录，如 `-o pics` 将图片保存到 `pics` 目录下

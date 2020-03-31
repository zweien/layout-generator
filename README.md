# layout-generator

[![Build Status](https://www.travis-ci.org/zweien/layout-generator.svg?branch=master)](https://www.travis-ci.org/zweien/layout-generator)
[![codecov](https://codecov.io/gh/zweien/layout-generator/branch/master/graph/badge.svg)](https://codecov.io/gh/zweien/layout-generator)

布局数据生成器，按需求生成热源组件布局-稳态温度场数据集。

![](https://i.bmp.ovh/imgs/2020/03/47d860f83ed75a99.png)

## 功能需求

- 可配置选项
  - [x] 布局板大小、边界要求
  - [ ] 组件配置
    - [x] 大小
    - [x] 数量
    - [ ] 形状
    - [x] 功率
  - 采样方式
    - [x] 均匀采样
  - fenics 求解器
    - [x] 均匀网格
    - [x] 网格分辨率
    - [x] 边界设置
    - [x] 多条边界
    - [x] 有限元 degree
  - 数据集存储
    - [x] 文件前缀
    - [x] mat 格式
    - [ ] 图片形式
- 数据集可视化 `layout_plot`
  - [x] 单一文件
  - [x] 目录批量处理
  - [x] multiprocess
- 性能
  - [x] multiprocess
  - [ ] cluster

## 已实现功能

- 配置文件与命令行两种使用方式
- 矩形组件离散位置摆放
  - 数量、位置、功率
- 可添加多条 Dirichlet 边界条件（开口）
- 使用 `fenics` 求解 Poisson 方程
  - 分辨率、有限元 degree
- 线性叠加原理求解 `--method fenics_additive`
- 数据集可视化脚本 `layout_plot`
- 多线程支持

## 安装方式

本生成器依赖 fenics 作为有限元求解器，参照 [fenics 安装文档](https://fenicsproject.org/download/)，推荐以下方式

- Docker
- Anaconda (**linux**)

  1. 使用 `conda` 创建并激活环境

  ```bash
  conda create -n fenicsproject -c conda-forge fenics mshr jupyter
  source activate fenicsproject
  ```

  2. 使用 pip 安装本 package

  ```bash
  pip install git+https://git.idrl.site/idrl/layout-generator.git
  ```

  3. 使用配置文件或命令行生成数据集，比如以默认配置文件 `default.yml` 生成数据集

  ```bash
  layout_generator
  ```

  其中 `default.yml` 在目录 `utils` 下。

## 用法

- 配置文件以 YAML 格式存储
- `layout_generator -h` 获取命令行帮助

```
usage: layout_generator [-h] [--config CONFIG] [--test] [--length LENGTH]
                        [--length_unit LENGTH_UNIT] [--bcs BCS]
                        [--power POWER] [--data_dir DATA_DIR]
                        [--sampler {uniform}] [--fem_degree FEM_DEGREE]
                        [--u_D U_D] [--unit_n UNIT_N] [--nx NX] [--ny NY]
                        [--sample_n SAMPLE_N] [--seed SEED]
                        [--file_format {mat}] [--prefix PREFIX]
                        [--method {fenics,fenics_additive}]

Generate layout dataset. Args that start with '--' (eg. --test) can also be
set in a config file (/home/fenics/shared/layout-
generator/layout_generator/utils/default.yml or specified via --config).
Config file syntax allows: key=value, flag=true, stuff=[a,b,c] (for details,
see syntax at https://goo.gl/R74nmi). If an arg is specified in more than one
place, then commandline values override config file values which override
defaults.

optional arguments:
  -h, --help            show this help message and exit
  --config CONFIG       config file path
  --test                test mode
  --length LENGTH       board length
  --length_unit LENGTH_UNIT
                        unit length
  --bcs BCS             Dirichlet boundarys, use two points to represent a
                        line segment
  --power POWER         possible powers of each unit
  --data_dir DATA_DIR   dir to store generated layout data
  --sampler {uniform}   sampler method
  --fem_degree FEM_DEGREE
                        fem degree in fenics
  --u_D U_D             value on Dirichlet boundary
  --unit_n UNIT_N       number of units
  --nx NX               number of grid in x direction
  --ny NY               number of grid in y direction
  --sample_n SAMPLE_N   number of samples
  --seed SEED           seed in np.random module
  --file_format {mat}   dataset file format
  --prefix PREFIX       prefix of file
  --method {fenics,fenics_additive}
                        method to solve the equation
```

- 默认参数

```yml
# config example

length: 0.1 # board 边长
length_unit: 0.01 # 组件边长
power: [10000, 20000] # 功率
u_D: 298 # 边界上取值
unit_n: 1 # 组件个数
# 边界位置，此处为两个边界，每个边界有两个点表示线段
bcs: "[ [[0.01, 0], [0.02, 0]], [[0.08, 0], [0.09, 0]] ]"
data_dir: example_dataset # 生成数据集的保存目录
file_format: mat # 数据集格式
prefix: Example # 单个数据的文件名前缀
sampler: uniform # 采样方法
sample_n: 2 # 生成数据个数
seed: 100 # 随机种子

fem_degree: 1 # 有限元 degree
nx: 21 # 生成数据 x 方向分辨率
ny: 21 # 生成数据 x 方向分辨率

method: fenics # 默认直接求解（fenics），也可以采用线性叠加原理（fenics_additive）
```

- 可视化脚本 `layout_plot`

```
λ layout_plot -h
usage: layout_plot [-h] [-p PATH] [-o OUTPUT] [--plot-off] [--dir]
                   [--worker WORKER]

optional arguments:
  -h, --help            show this help message and exit
  -p PATH, --path PATH  file path
  -o OUTPUT, --output OUTPUT
                        output path
  --plot-off            turn off plot
  --dir                 path is dir
  --worker WORKER       number of workers
```

### 例子

1. 在 `./data1` 目录下生成 100 个数据，图像分辨率为 30\*30，底边中间开口 1/4 边长，每个布局有 3 个组件，其他参数使用如上默认参数：

```bash
layout_generator --data_dir data1 --sample_n 100 --nx 30 --ny 30 --bcs "[ [[0.0375, 0], [0.0625, 0]] ]" --unit_n 3
```

2. 可视化 `./data1` 目录下生成好的数据
   1. 转化单个数据文件`./data1/Example0.mat`，在相同目录下生成 png 文件, `layout_plot -p data1/Example0.mat --plot-off`
   2. 以 4 线程转化整个目录，`layout_plot -p data1 --dir --worker 4`

### 参数说明

- bcs: Dirichlet 边界 (对应布局问题中的开孔)，以嵌套 list 的形式配置。可以设置多条边界，每条边界用两个点(A, B)表示线段 `[[Ax, Ay], [Bx, By]]`。
  - 若四周全开孔，可设置 `bc: "[]"`
- power: 组件功率，可设置多种功率大小


## Change Log

- v0.2.0
  - 增加 3D 数据生成
    - 统一入口 `layout_generator`
    - 3D poisson solver 
    - vtk 数据存储
- v0.1.2
  - 布局预处理，fenics solver 增速
  - 修改默认参数 method: fenics
  - 增加可视化脚本 `layout_plot`
    - 单一文件 plot，保存
    - 目录装换
  - multiprocess 支持，增加 worker 参数
- v0.1.1
  - 增加命令行入口
  - 增加配置测试模式
  - 更新 setup.py
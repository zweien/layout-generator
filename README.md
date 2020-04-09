# layout-generator

[![Build Status](https://www.travis-ci.org/zweien/layout-generator.svg?branch=master)](https://www.travis-ci.org/zweien/layout-generator)
[![codecov](https://codecov.io/gh/zweien/layout-generator/branch/master/graph/badge.svg)](https://codecov.io/gh/zweien/layout-generator)
[![CodeFactor](https://www.codefactor.io/repository/github/zweien/layout-generator/badge)](https://www.codefactor.io/repository/github/zweien/layout-generator)

布局数据生成器，按需求生成热源组件布局-稳态温度场数据集。

![](https://i.bmp.ovh/imgs/2020/03/47d860f83ed75a99.png)
![](https://i.bmp.ovh/imgs/2020/04/acda55376056bc8f.png)

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
    - [x] 线性叠加原理
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

本生成器依赖 fenics 作为有限元求解器，可参照 [fenics 安装文档](https://fenicsproject.org/download/)，推荐以下方式

- Docker (**linux**, **win**)
  1. 安装 docker-ce (若已有 docker 可跳过)
  2. pull fenics image: `docker pull quay.azk8s.cn/fenicsproject/stable`
  3. 创建并启动容器: `docker run -it -v $(pwd):/home/fenics/shared -u root quay.azk8s.cn/fenicsproject/stable bash`
  4. 使用 pip 安装本 package
  ```bash
  pip install git+https://git.idrl.site/idrl/layout-generator.git
  ```
- Anaconda (**linux**)

  1. 使用 `conda` 创建并激活环境

  ```bash
  conda create -n fenicsproject -c conda-forge fenics mshr
  source activate fenicsproject
  ```

  1. 使用 pip 安装本 package

  ```bash
  pip install git+https://git.idrl.site/idrl/layout-generator.git
  ```

## 用法

- 使用配置文件或命令行生成数据集，比如以默认配置文件 `default.yml` 生成数据集

```bash
layout_generator
```

其中 `default.yml` 在目录 `utils` 下。

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

ndim: 2 # dimension
length: 0.1
length_unit: 0.01
power: [10000]
u_D: 298
unit_n: 1
# bcs: "[ [[0.01, 0], [0.02, 0]], [[0.08, 0], [0.09, 0]] ]" # 2d example
# bcs: "[ [[0, 0.05, 0.05], [0, 0.07, 0.07]]]" # 3d example
bcs: "[]" # all are Dirichlet BCs
data_dir: example_dataset
file_format: mat
prefix: Example
sampler: uniform
sample_n: 2
seed: 100

fem_degree: 1
nx: 21
# ny: 21
# nz: 21

method: fenics
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

1. 针对 2D 问题，在 `./data1` 目录下生成 100 个数据，图像分辨率为 30\*30，底边中间开口 1/4 边长，每个布局有 3 个组件，其他参数使用如上默认参数：

```bash
layout_generator --data_dir data1 --sample_n 100 --nx 30 --ny 30 --bcs "[ [[0.0375, 0], [0.0625, 0]] ]" --unit_n 3
```

2. 可视化 `./data1` 目录下生成好的数据
   1. 转化单个数据文件`./data1/Example0.mat`，在相同目录下生成 png 文件, `layout_plot -p data1/Example0.mat --plot-off`
   2. 以 4 线程转化整个目录，`layout_plot -p data1 --dir --worker 4`

### 参数说明

- bcs: Dirichlet 边界 (对应布局问题中的开孔)，以嵌套 list 的形式配置。
  - 可以设置多条边界
  - 2D: 每条边界用两个点 (A, B)表示线段 `[[Ax, Ay], [Bx, By]]`。
  - 3D: 每个边界用矩形表示，用两个对角点 (A, B) 表示矩形 `[[Ax, Ay, Az], [Bx, By, Bz]]`。
  - 若所有边界全为 Dirichlet 类型，可设置 `bc: "[]"`
- power: 组件功率，可设置多种功率大小

## Change Log

- v0.2.1
  - 修改配置文件中 bcs
  - 重构部分代码
  - 增加单元测试
- v0.2.0
  - 增加 3D 数据生成
    - 统一入口 `layout_generator`
    - 实现 3D Poisson solver
    - vtk 数据存储
- v0.1.2
  - 布局预处理，改进 fenics solver 性能
  - 修改默认参数 method: fenics
  - 增加可视化脚本 `layout_plot`
    - 单一文件 plot，保存
    - 目录装换
  - multiprocess 支持，增加 worker 参数
- v0.1.1
  - 增加命令行入口
  - 增加配置测试模式
  - 更新 setup.py

# 连续布局

均匀矩形组件、离散布局生成器。

![](https://i.bmp.ovh/imgs/2020/03/47d860f83ed75a99.png)
![](https://i.bmp.ovh/imgs/2020/04/acda55376056bc8f.png)

## 用法

- 使用配置文件或命令行生成数据集，比如以默认配置文件 `default_c.yml` 生成数据集

```bash
layout_generator_c
```

其中 `default_c.yml` 在目录 `utils` 下。

- 配置文件以 YAML 格式存储
- `layout_generator_c -h` 获取命令行帮助

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
  --bcs BCS             Dirichlet boundaries, use two points to represent a
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
# bcs:
#     - [[0.01, 0], [0.02, 0]]
#     - [[0.08, 0], [0.09, 0]] # 2d example
# bcs:
#     - [[0, 0.05, 0.05], [0, 0.07, 0.07]]  # 3d example
bcs: [] # all are Dirichlet BCs
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
$ layout_plot -h
usage: layout_generator [-h] [--config CONFIG] [--test] [--length LENGTH]
                        [--length_unit LENGTH_UNIT] [--bcs BCS]
                        [--power POWER] [--data_dir DATA_DIR]
                        [--sampler {uniform}] [--fem_degree FEM_DEGREE]
                        [--u_D U_D] [--unit_n UNIT_N] [--nx NX]
                        [--sample_n SAMPLE_N] [--seed SEED]
                        [--file_format {mat}] [--prefix PREFIX]
                        [--method {fenics}] [--worker WORKER] [--ndim {2,3}]
                        [--vtk]

Generate layout dataset. Args that start with '--' (eg. --test) can also be
set in a config file (/home/fenics/shared/layout-
generator/layout_generator/utils/default.yml or specified via --config). The
config file uses YAML syntax and must represent a YAML 'mapping' (for details,
see http://learn.getgrav.org/advanced/yaml). If an arg is specified in more
than one place, then commandline values override config file values which
override defaults.

optional arguments:
  -h, --help            show this help message and exit
  --config CONFIG       config file path
  --test                test mode
  --length LENGTH       board length
  --length_unit LENGTH_UNIT
                        unit length
  --bcs BCS             Dirichlet boundarys
  --power POWER         possible power of each unit
  --data_dir DATA_DIR   dir to store generated layout data
  --sampler {uniform}   sampler method
  --fem_degree FEM_DEGREE
                        fem degree in fenics
  --u_D U_D             value on Dirichlet boundary
  --unit_n UNIT_N       number of units
  --nx NX               number of grid in x direction
  --sample_n SAMPLE_N   number of samples
  --seed SEED           seed in np.random module
  --file_format {mat}   dataset file format
  --prefix PREFIX       prefix of file
  --method {fenics}     method to solve the equation
  --worker WORKER       number of workers
  --ndim {2,3}          dimension
  --vtk                 output vtk file
```

### 例子

1. 针对 2D 问题，在 `./data1` 目录下生成 100 个数据，图像分辨率为 30\*30，底边中间开口 1/4 边长，每个布局有 3 个组件，其他参数使用如上默认参数：

```bash
layout_generator --data_dir data1 --sample_n 100 --nx 30 --bcs [[0.0375,0],[0.0625,0]] --unit_n 3
```

2. 可视化 `./data1` 目录下生成好的数据
   1. 转化单个数据文件`./data1/Example0.mat`，在相同目录下生成 png 文件, `layout_plot -p data1/Example0.mat --plot-off`
   2. 以 4 线程转化整个目下的文件，`layout_plot -p data1 --dir --worker 4`

### 参数说明

- bcs: Dirichlet 边界 (对应布局问题中的开孔)，以嵌套 list 的形式配置。
  - 可设置多个边界，在 yml 配置文件中每行表示一个边界
  ```yml
  bcs:
    - [[0.01, 0], [0.02, 0]]
    - [[0.08, 0], [0.09, 0]] # 2d example
  ```
  - 2D: 每条边界用两个点 (A, B)表示线段 `[[Ax, Ay], [Bx, By]]`。
  - 3D: 每个边界用矩形表示，用两个对角点 (A, B) 表示矩形 `[[Ax, Ay, Az], [Bx, By, Bz]]`。
  - 若所有边界全为 Dirichlet 类型，可设置 `bc: []`
- power: 组件功率，可设置多种功率大小
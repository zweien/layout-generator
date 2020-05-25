# 离散布局

均匀矩形组件、离散布局生成器，使用脚本`layout_generator generate` 配合**配置文件**与**命令行参数**生成所**布局图像**与**温度场**数据。

![](https://i.bmp.ovh/imgs/2020/03/47d860f83ed75a99.png)
![](https://i.bmp.ovh/imgs/2020/04/acda55376056bc8f.png)

## 用法

1. 使用配置文件或命令行生成数据集，比如以默认配置文件 `default.yml` 生成数据集，其中 `default.yml` 在目录 `utils` 下。
1. 或使用自定义配置文件 `--config 配置文件路径`
   - 配置文件以 YAML 格式存
1. 优先级：命令行参数 > 配置文件参数 > 默认参数

- `layout_generator generate -h` 获取脚本帮助
```text
usage: layout_generator generate [-h] [--config CONFIG] [--test]
                                 [--length LENGTH] [--length_unit LENGTH_UNIT]
                                 [--bcs BCS] [--data_dir DATA_DIR]
                                 [--fem_degree FEM_DEGREE] [--u_D U_D]
                                 [--nx NX] [--sample_n SAMPLE_N] [--seed SEED]
                                 [--file_format {mat}] [--prefix PREFIX]
                                 [--method {fenics}] [--worker WORKER]
                                 [--ndim {2,3}] [--vtk] [-V]
                                 [--task {discrete,continuous}]
                                 [--power POWER] [--unit_n UNIT_N]
                                 [--sampler {uniform}]

Args that start with '--' (eg. --test) can also be set in a config file
(/home/fenics/shared/layout-generator/layout_generator/utils/default.yml or
specified via --config). The config file uses YAML syntax and must represent a
YAML 'mapping' (for details, see http://learn.getgrav.org/advanced/yaml). If
an arg is specified in more than one place, then commandline values override
config file values which override defaults.

optional arguments:
  -h, --help            show this help message and exit
  --config CONFIG       config file path
  --test                test mode
  --length LENGTH       board length
  --length_unit LENGTH_UNIT
                        unit length
  --bcs BCS             Dirichlet boundaries
  --data_dir DATA_DIR   dir to store generated layout data
  --fem_degree FEM_DEGREE
                        fem degree in fenics
  --u_D U_D             value on Dirichlet boundary
  --nx NX               number of grid in x direction
  --sample_n SAMPLE_N   number of samples
  --seed SEED           seed in np.random module
  --file_format {mat}   dataset file format
  --prefix PREFIX       prefix of file
  --method {fenics}     method to solve the equation
  --worker WORKER       number of workers
  --ndim {2,3}          dimension
  --vtk                 output vtk file
  -V, --version         show program's version number and exit
  --task {discrete,continuous}
                        task
  --power POWER         possible power of each unit
  --unit_n UNIT_N       number of units
  --sampler {uniform}   sampler method
```

- 默认配置文件参数 (yaml)

```yaml
# config example

task: discrete
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
bcs: [[]]  # all are Dirichlet BCs
data_dir: example_dataset
file_format: mat
prefix: Example
sampler: uniform
sample_n: 2
# seed: 100

fem_degree: 1
nx: 21
# ny: 21
# nz: 21

method: fenics
```


### 示例

1. 在当前目录下准备配置文件 `config.yml`，使用该配置文件生成相应数据集:
```bash
layout_generator generate --config config.yml
```
2. 针对 2D 问题，在 `./data1` 目录下生成 100 个数据，图像分辨率为 30\*30，底边中间开口 1/4 边长，每个布局有 3 个组件，其他参数使用如上默认参数：

```bash
layout_generator generate --data_dir data1 --sample_n 100 --nx 30 --bcs [[0.0375,0],[0.0625,0]] --unit_n 3
```



### 参数说明

- bcs: Dirichlet 边界 (对应布局问题中的开孔)，以嵌套 list 的形式配置。
  - 可设置多个边界，在 yml 配置文件中每行表示一个边界
  ```yaml
  bcs:
    - [[0.01, 0], [0.02, 0]]
    - [[0.08, 0], [0.09, 0]] # 2d example
  ```
  - 2D: 每条边界用两个点 (A, B)表示线段 `[[Ax, Ay], [Bx, By]]`。
  - 3D: 每个边界用矩形表示，用两个对角点 (A, B) 表示矩形 `[[Ax, Ay, Az], [Bx, By, Bz]]`。
  - 若所有边界全为 Dirichlet 类型，可设置 `bc: [[]]`
- power: 组件功率，可设置多种功率大小
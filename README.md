# layout-generator
![travis](https://api.travis-ci.com/zweien/layout-generator.svg)

布局数据生成器，按需求生成热源组件布局-稳态温度场数据集。

## 功能需求

- 可配置选项
  - [x] 布局板大小、边界要求
  - [ ] 组件配置
    - [x] 大小
    - [x] 数量
    - [ ] 形状
    - [ ] 功率
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

## 已实现功能

- 配置文件与命令行两种使用方式
- 矩形组件离散位置摆放
  - 数量、位置、功率
- 可添加多条 Dirichlet 边界条件（开口）
- 使用 `fenics` 求解 Poisson 方程
  - 分辨率、有限元 degree
- 线性叠加原理求解 `--method fenics_additive`

## 安装方式

本生成器依赖 fenics 作为有限元求解器，参照 [fenics安装文档](https://fenicsproject.org/download/)，推荐以下方式
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

![](https://i.bmp.ovh/imgs/2020/03/b2104e86c55e5320.png)

- 默认参数
```yml
# config example

length: 0.1 # board 边长
length_unit: 0.01  # 组件边长
power: 10000  # 功率
u_D: 298  # 边界上取值
unit_n: 1  # 组件个数
# 边界位置，此处为两个边界，每个边界有两个点表示线段
bcs: "[ [[0.01, 0], [0.02, 0]], [[0.08, 0], [0.09, 0]] ]"
data_dir: example_dataset  # 生成数据集的保存目录
file_format: mat  # 数据集格式
prefix: Example  # 单个数据的文件名前缀
sampler: uniform  # 采样方法
sample_n: 2  # 生成数据个数
seed: 100  # 随机种子

fem_degree: 1  # 有限元 degree
nx: 10  # 生成数据 x 方向分辨率
ny: 10  # 生成数据 x 方向分辨率

method: fenics_additive  # 默认使用线性叠加原理，也可直接求解（fenics），但目前效率较差
```

### 例子

1. 在 `./data1` 目录下生成 100 个数据，分辨率为 30*30，底边中间开口 1/4 边长，每个布局有 3 个组件，其他参数使用如上默认参数：
```bash
layout_generator --data_dir data1 --sample_n 100 --nx 30 --ny 30 --bcs "[ [[0.0375, 0], [0.0625, 0]] ]" --unit_n 3
```

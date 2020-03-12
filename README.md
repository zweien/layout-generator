# layout-generator

布局数据生成器，按需求生成热源组件布局-稳态温度场数据集。

## 功能需求

- 可配置选项
  - 布局板大小、边界要求
  - 组件形状、大小、功率、数量
  - 采样方式，数量
  - fenics 求解器
    - 网格剖分
    - 有限元解空间
  - 数据集存储格式

## 已实现功能

- 使用 `fenics` 求解 Poisson 方程
- 组件离散位置摆放
- 添加多条 Dirichlet 边界条件（开口）
- 线性叠加原理求解 `--method fenics_additive`

## 使用方式

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
  3. 以模块运行方式，使用配置文件或命令行生成数据集，比如
  ```bash
  python -m layout_generator --config default.yml
  ```
  其中 `default.yml` 在本仓库 `configs` 目录下。
  
## 用法

- 配置文件以 YAML 格式存储
- `python -m layout_generator -h` 获取命令行帮助

![](https://i.bmp.ovh/imgs/2020/03/3721a692143eedee.png)




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

- ...

## 使用方式

本生成器依赖 fenics 作为有限元求解器，参照 [fenics安装文档](https://fenicsproject.org/download/)，推荐以下方式
- Docker
- Anaconda (**linux**)
  1. 使用 `conda` 创建环境 
    ```bash
    conda create -n fenicsproject -c conda-forge fenics jupyter
    source activate fenicsproject
    ```

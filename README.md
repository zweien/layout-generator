# layout-generator

[![Build Status](https://www.travis-ci.org/zweien/layout-generator.svg?branch=master)](https://www.travis-ci.org/zweien/layout-generator)
[![codecov](https://codecov.io/gh/zweien/layout-generator/branch/master/graph/badge.svg)](https://codecov.io/gh/zweien/layout-generator)
[![CodeFactor](https://www.codefactor.io/repository/github/zweien/layout-generator/badge)](https://www.codefactor.io/repository/github/zweien/layout-generator)
[![readthedocs](https://readthedocs.org/projects/layout-data/badge/)](https://layout-generator.readthedocs.io/zh/latest/)
[![GitLicense](https://gitlicense.com/badge/zweien/layout-generator)](https://gitlicense.com/license/zweien/layout-generator)
![Upload Python Package](https://github.com/zweien/layout-generator/workflows/Upload%20Python%20Package/badge.svg)
![Publish Docker Releases](https://github.com/zweien/layout-generator/workflows/Publish%20Docker%20Releases/badge.svg)

布局数据生成器 layout-generator，可按需求生成热源**组件布局-稳态温度场**数据集。

**文档**：[ReadTheDocs](https://layout-generator.readthedocs.io/zh/latest/)

![](https://i.bmp.ovh/imgs/2020/03/47d860f83ed75a99.png)
![](https://i.bmp.ovh/imgs/2020/04/acda55376056bc8f.png)

## 功能需求

- 可配置选项
  - [x] 布局板大小、边界要求
  - [x] 组件配置
    - [x] 大小
    - [x] 数量
    - [x] 形状
    - [x] 功率
  - 采样方式
    - 离散布局
      - [x] 均匀采样
    - 连续布局
      - [x] 顺序摆放采样
      - [x] Gibbs 采样 
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
    - [x] HDF5
    - [ ] 图片形式
  - 其他
    - [x] 随机数种子
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
- 固定组件位置，变功率采样
- 矩形组件连续位置摆放
- 可添加多条 Dirichlet 边界条件（开口）
- 使用 `fenics` 求解 Poisson 方程
  - 分辨率、有限元 degree
- 数据集可视化脚本 `layout_plot`
- 多线程支持
- 统一脚本入口

## 安装方式

本生成器依赖 fenics 作为有限元求解器，可参照 [fenics 安装文档](https://fenicsproject.org/download/)，推荐以下**两种**方式安装，如果没有没有 docker 使用经验推荐 Anaconda 方式

- Anaconda (**Linux**， **Mac**)
  1. 使用 `conda` 创建并激活环境
  ```text
  conda create -n fenicsproject -c conda-forge fenics mshr
  source activate fenicsproject
  ```
  2. use pip to install the released version
     - `pip install -U layout-generator`
     - or use unreleased version from master branch
      ```text
      pip install -U git+https://github.com/zweien/layout-generator.git
      ```

- Docker (**Linux**, **Win**, **Mac**)
  - 从 dockerhub 拉取镜像 `docker pull zweien/layout-generator:latest`
    1. 切换到需要生成数据集的目录，准备好配置文件 `config.yml`
    2. 使用 `config.yml` 在当前目录下生成数据集，数据集所在文件夹为 `data1`
    ```text
    docker run --rm layout-generator:latest -v $(pwd):/home/fenics/layout layout_generater generate --config config.yml --data_dir data1
    ```
    Notes：windows 下 cmd 中使用 `-v %cd%:/home/fenics/layout`


## FAQ

- Windows 下可以使用 Docker 方式安装，或在应用商店安装 Ubuntu WSL
- pip 安装前可使用国内源如清华 
  ```text
  pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple
  ```
- 如果出现 HDF5 error，请使用如下命令重新安装 `h5py`
  ```text
  pip uninstall h5py
  pip install --no-binary=h5py h5py
  ```
- 仅支持 Python3.6 以上版本
- 如果按照以上 anaconda 安装方式，别忘了切换到 `fenicsproject` 环境

## 使用方法

请参见[文档](https://layout-generator.readthedocs.io/zh/latest/)


## Change Log

- v0.6.0
  - add 固定组件位置，变功率采样
  - add `layout_generator.generator.layout_pos2temp()`
  - add `laytout_generator.sampler.continuous.base.Task.layout_from_pos()`
  - add `layout_generator.generator.layout_pos_list2temp()` for generating a sample according to paticular layout position list
  - add command `makeconfig` for generating template config
- v0.5.3
  - fix bug in sequence sampling
- v0.5.2
  - update installation guide
  - add github action for pushing images to dockerhub
- v0.5.1
  - fix file config.xml empty error
  - add PyPi for installing
  - add github action for publishing to PyPi
- v0.5.0
  - 统一脚本入口 `layout_generator`
    - 离散布局 `layout_generator generate`
    - 连续布局 `layout_generator generate_c`
    - 可视化 `layout_generator plot`
    - 转换数据格式 `layout_generator convert`
  - 连续布局增加单个组件多种备选功率配置
- v0.4.2
  - 删除默认 seed
- v0.4.1
  - 增加 Dockerfile
  - 更新安装方式
  - 更新文档
- v0.4.0
  - 增加连续布局 gibbs 采样
  - 重构连续采样代码
  - 增加 FAQ
- v0.3.0
  - 增加连续布局生成脚本 `layout-generator_c`
  - 增加单元测试
  - 文档迁移
- v0.2.2
  - 增加转换脚本 `layout_convert`，实现 mat 到 HDF5 格式的转换
  - 修复bug `--bcs []` 
  - 增加单元测试
  - 更新依赖
- v0.2.1
  - 修改配置文件中 bcs 配置方式
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

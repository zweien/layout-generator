# layout-generator

[![Build Status](https://www.travis-ci.org/zweien/layout-generator.svg?branch=master)](https://www.travis-ci.org/zweien/layout-generator)
[![codecov](https://codecov.io/gh/zweien/layout-generator/branch/master/graph/badge.svg)](https://codecov.io/gh/zweien/layout-generator)
[![CodeFactor](https://www.codefactor.io/repository/github/zweien/layout-generator/badge)](https://www.codefactor.io/repository/github/zweien/layout-generator)
[![readthedocs](https://readthedocs.org/projects/layout-data/badge/)](https://layout-generator.readthedocs.io/zh/latest/)
[![GitLicense](https://gitlicense.com/badge/zweien/layout-generator)](https://gitlicense.com/license/zweien/layout-generator)

layout-generator 为布局数据生成器，可按需求生成热源**组件布局-稳态温度场**数据集。

**文档**：[ReadTheDocs](https://layout-data.readthedocs.io/zh/latest/)

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
    - [x] HDF5
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
- 矩形组件连续位置摆放
- 可添加多条 Dirichlet 边界条件（开口）
- 使用 `fenics` 求解 Poisson 方程
  - 分辨率、有限元 degree
- 数据集可视化脚本 `layout_plot`
- 多线程支持

## 安装方式

本生成器依赖 fenics 作为有限元求解器，可参照 [fenics 安装文档](https://fenicsproject.org/download/)，推荐以下方式

- Docker (**linux**, **win**)
  1. 安装 [docker-ce](https://docs.docker.com/) (若已安装 docker 可跳过)
  2. pull fenics image (docker hub 中国 Azure 源): `docker pull quay.azk8s.cn/fenicsproject/stable`
  3. 创建并启动容器: `docker run -it -v $(pwd):/home/fenics/shared -u root quay.azk8s.cn/fenicsproject/stable bash`
  4. 使用 pip 安装本 package
  ```bash
  pip install git+https://git.idrl.site/idrl/layout-generator.git
  ```
- Anaconda (**linux**， **Mac**)
  1. 使用 `conda` 创建并激活环境
  ```bash
  conda create -n fenicsproject -c conda-forge fenics mshr
  source activate fenicsproject
  ```
  2. 使用 pip 安装本 package
  ```bash
  pip install -U git+https://git.idrl.site/idrl/layout-generator.git
  ```


## Change Log

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

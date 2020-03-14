# layout-generator

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
  - 数据集存储格式
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
  3. 使用配置文件或命令行生成数据集，比如以默认配置文件 `default.yml` 生成数据集
  ```bash
  layout_generator
  ```
  其中 `default.yml` 在目录 `utils` 下。
  
## 用法

- 配置文件以 YAML 格式存储
- `layout_generator -h` 获取命令行帮助

![](https://i.bmp.ovh/imgs/2020/03/b2104e86c55e5320.png)



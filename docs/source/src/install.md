# 安装

本生成器依赖 fenics 作为有限元求解器，可参照 [fenics 安装文档](https://fenicsproject.org/download/)，推荐以下**两种**方式安装，如果没有没有 docker 使用经验推荐 Anaconda 方式

## Anaconda

- Anaconda (**Linux**, **Mac**)
  1. 使用 `conda` 创建并激活环境
  ```text
  conda create -n fenicsproject -c conda-forge fenics mshr
  source activate fenicsproject
  ```
  2. 使用 pip 安装本 package
  ```text
  pip install -U git+https://git.idrl.site/idrl/layout-generator.git
  ```

## Docker

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
- pip 安装前可使用国内源如清华、阿里 
  ```
  pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple
  ```
- 如果出现 `HDF5 error`，请使用如下命令重新安装 `h5py`
  ```text
  pip uninstall h5py
  pip install --no-binary=h5py h5py
  ```
- 目前仅支持 Python3.6 以上版本
- 如果按照以上 Anaconda 安装方式，别忘了切换到 `fenicsproject` 环境
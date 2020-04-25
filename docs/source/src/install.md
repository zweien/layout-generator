# 安装

本生成器依赖 fenics 作为有限元求解器，可参照 [fenics 安装文档](https://fenicsproject.org/download/)，推荐以下方式

## Docker

- Docker (**linux**, **win**)
  1. 安装 [docker-ce](https://docs.docker.com/) (若已安装 docker 可跳过)
  2. pull fenics image (docker hub 中国 Azure 源): `docker pull quay.azk8s.cn/fenicsproject/stable`
  3. 创建并启动容器: `docker run -it -v $(pwd):/home/fenics/shared -u root quay.azk8s.cn/fenicsproject/stable bash`
  4. 使用 pip 安装本 package
  ```bash
  pip install git+https://git.idrl.site/idrl/layout-generator.git
  ```

## Anaconda

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
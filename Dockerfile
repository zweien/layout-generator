From quay.azk8s.cn/fenicsproject/stable:current
MAINTAINER zweien <278954153@qq.com>

WORKDIR /tmp
COPY . .
RUN pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple && pip install .
RUN useradd --create-home --no-log-init --shell /bin/bash layout
USER layout
WORKDIR /home/layout
ENTRYPOINT [""]

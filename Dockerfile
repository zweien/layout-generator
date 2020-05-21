From quay.azk8s.cn/fenicsproject/stable:current
MAINTAINER zweien <278954153@qq.com>

WORKDIR /tmp
COPY . .
RUN pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple && pip install . && rm -rf *

USER fenics
RUN mkdir /home/fenics/layout
WORKDIR /home/fenics/layout
RUN layout_generator --worker 1 && rm -rf *
ENTRYPOINT [""]

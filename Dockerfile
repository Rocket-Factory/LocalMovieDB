# syntax=docker/dockerfile:1
FROM ubuntu:focal-20220426

ENV TZ=Asia/Shanghai
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

WORKDIR /app

COPY . .
RUN sudo apt update
RUN apt install -y python3 python3-dev python3-pip
RUN sudo apt install -y nginx

RUN pip3 config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple
RUN pip3 install -r requirements.txt

RUN python3 init.py
RUN service nginx restart

CMD python3 app.py

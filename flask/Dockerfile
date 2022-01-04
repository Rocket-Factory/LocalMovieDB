# syntax=docker/dockerfile:1
FROM python:3.7-slim

EXPOSE 5006

WORKDIR /app

COPY . .

COPY requirements.txt requirements.txt
RUN pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple
RUN pip3 install -r requirements.txt

CMD python3 app.py

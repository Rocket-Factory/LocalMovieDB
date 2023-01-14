# syntax=docker/dockerfile:1
FROM ubuntu:focal-20220426

ENV TZ=Asia/Shanghai
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

WORKDIR /app

COPY . .

# prepare environment
# error when build in arm machine
# RUN mv docker_things/ubuntu_focal_sources.list /etc/apt/sources.list
# RUN chmod 664 /etc/apt/sources.list
RUN apt update
RUN apt install -y python3 python3-dev python3-pip nginx wget gcc openssl libssl-dev libpcre3 libpcre3-dev zlib1g-dev make

# install nginx
RUN wget http://nginx.org/download/nginx-1.18.0.tar.gz
RUN tar -zxvf nginx-1.18.0.tar.gz
WORKDIR /app/nginx-1.18.0/
RUN cd /app/nginx-1.18.0/
RUN /app/nginx-1.18.0/configure --with-cc-opt='-g -O2 -fdebug-prefix-map=/build/nginx-7KvRN5/nginx-1.18.0=. -fstack-protector-strong -Wformat -Werror=format-security -fPIC -Wdate-time -D_FORTIFY_SOURCE=2' --with-ld-opt='-Wl,-Bsymbolic-functions -Wl,-z,relro -Wl,-z,now -fPIC' --prefix=/usr/share/nginx --conf-path=/etc/nginx/nginx.conf --http-log-path=/var/log/nginx/access.log --error-log-path=/var/log/nginx/error.log --lock-path=/var/lock/nginx.lock --pid-path=/run/nginx.pid --modules-path=/usr/lib/nginx/modules --http-client-body-temp-path=/var/lib/nginx/body --http-fastcgi-temp-path=/var/lib/nginx/fastcgi --http-proxy-temp-path=/var/lib/nginx/proxy --http-scgi-temp-path=/var/lib/nginx/scgi --http-uwsgi-temp-path=/var/lib/nginx/uwsgi --with-debug --with-compat --with-pcre-jit --with-http_ssl_module --with-http_stub_status_module --with-http_realip_module --with-http_auth_request_module --with-http_v2_module --with-http_dav_module --with-http_slice_module --with-threads --with-http_addition_module --with-http_gunzip_module --with-http_gzip_static_module --with-http_sub_module --with-stream=dynamic --with-stream_ssl_module --with-mail=dynamic --with-mail_ssl_module --with-http_secure_link_module
RUN make
RUN mv /app/nginx-1.18.0/objs/nginx /usr/sbin/nginx
RUN chmod +x /usr/sbin/nginx

# run app
WORKDIR /app
RUN cd /app
# RUN pip3 config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple
RUN pip3 install -r requirements.txt

RUN python3 init.py

CMD python3 app.py

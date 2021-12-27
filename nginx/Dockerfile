FROM nginx

RUN rm /etc/nginx/conf.d/default.conf

COPY nginx.conf /etc/nginx/conf.d/

# 修改user pass 为你的账号密码(与docker-compose.yml中一致)
RUN printf "user:$(openssl passwd -crypt pass)\n" >> /etc/nginx/htpasswd

EXPOSE 80
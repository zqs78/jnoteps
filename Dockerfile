# 使用一个极简的Linux基础镜像
FROM alpine:latest

# 安装一个轻量级的Web服务器，用于健康检查
RUN apk add --no-cache lighttpd

# 创建一个简单的健康检查页面
RUN echo "<html><body><h1>Service is Running</h1></body></html>" > /var/www/localhost/htdocs/index.html

# 暴露一个端口（先用8080，后面可以改）
EXPOSE 8080

# 启动Web服务器
CMD ["lighttpd", "-D", "-f", "/etc/lighttpd/lighttpd.conf"]

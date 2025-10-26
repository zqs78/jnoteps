FROM alpine:3.18

# 安装系统依赖
RUN apk update && apk add --no-cache \
    python3 \
    py3-pip \
    curl \
    unzip \
    ca-certificates \
    tzdata

# 安装Python依赖
RUN pip3 install --no-cache-dir aiohttp==3.9.0

# 下载并安装Xray
RUN cd /tmp && \
    curl -L -o xray.zip https://github.com/XTLS/Xray-core/releases/latest/download/Xray-linux-64.zip && \
    unzip xray.zip && \
    mv xray /usr/local/bin/ && \
    chmod +x /usr/local/bin/xray && \
    mkdir -p /usr/local/share/xray/ && \
    mv geoip.dat geosite.dat /usr/local/share/xray/ && \
    rm -f xray.zip

# 创建配置目录
RUN mkdir -p /etc/xray/

# 设置工作目录
WORKDIR /app

# 复制应用程序文件
COPY . .

# 关键修复：将配置文件复制到正确位置
RUN cp config.json /etc/xray/config.json

# 设置文件权限
RUN chmod +x start.sh

# 暴露端口
EXPOSE 20018 8000

# 启动命令
CMD ["./start.sh"]

FROM alpine:3.18

# 安装系统依赖
RUN apk update && apk add --no-cache \
    python3 \
    py3-pip \
    curl \
    unzip \
    ca-certificates \
    tzdata

# 安装 Python 依赖
RUN pip3 install --no-cache-dir aiohttp==3.9.0

# 下载并安装 Xray
RUN cd /tmp && \
    curl -L -o xray.zip https://github.com/XTLS/Xray-core/releases/latest/download/Xray-linux-64.zip && \
    unzip xray.zip && \
    mv xray /usr/local/bin/ && \
    chmod +x /usr/local/bin/xray && \
    mkdir -p /usr/local/share/xray/ && \
    mv geoip.dat geosite.dat /usr/local/share/xray/ && \
    rm -f xray.zip

# 设置工作目录
WORKDIR /app

# 复制应用程序文件
COPY . .

# 设置文件权限
RUN chmod +x start.sh

# 暴露端口
EXPOSE 20018 8000

# 健康检查
HEALTHCHECK --interval=30s --timeout=10s --start-period=30s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

# 启动命令
CMD ["./start.sh"]

FROM alpine:latest

RUN apk update && apk add --no-cache \
    python3 \
    py3-aiohttp \
    curl \
    unzip \
    ca-certificates

# 下载并安装 Xray，同时获取 geoip.dat 和 geosite.dat
RUN cd /tmp && \
    curl -L -o xray.zip https://github.com/XTLS/Xray-core/releases/latest/download/Xray-linux-64.zip && \
    unzip xray.zip && \
    mv xray /usr/local/bin/ && \
    chmod +x /usr/local/bin/xray && \
    # 关键修改：将数据文件移动到标准目录，而非删除它们
    mkdir -p /usr/local/share/xray/ && \
    mv geoip.dat geosite.dat /usr/local/share/xray/ && \
    rm -rf xray.zip  # 只删除ZIP包，保留数据文件

WORKDIR /app

COPY config.json /etc/xray/config.json
COPY main.py .
COPY start.sh .

RUN chmod +x /app/start.sh

EXPOSE 20018 8000

CMD ["/app/start.sh"]

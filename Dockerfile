FROM alpine:latest

RUN apk update && apk add --no-cache \
    python3 \
    py3-aiohttp \
    curl \
    unzip \
    ca-certificates \
    tzdata

# 下载并安装Xray核心文件，包括geoip.dat和geosite.dat
RUN cd /tmp && \
    curl -L -o xray.zip https://github.com/XTLS/Xray-core/releases/latest/download/Xray-linux-64.zip && \
    unzip xray.zip && \
    mv xray /usr/local/bin/ && \
    chmod +x /usr/local/bin/xray && \
    # 关键修改：保留geoip.dat和geosite.dat文件
    mkdir -p /usr/local/share/xray/ && \
    mv geoip.dat geosite.dat /usr/local/share/xray/ && \
    rm -rf xray.zip

WORKDIR /app

COPY config.json /etc/xray/config.json
COPY main.py .
COPY start.sh .

RUN chmod +x /app/start.sh

EXPOSE 20018 8000

HEALTHCHECK --interval=30s --timeout=10s --start-period=30s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

CMD ["/app/start.sh"]

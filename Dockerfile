FROM alpine:latest

RUN apk update && apk add --no-cache \
    python3 \
    py3-pip \
    curl \
    unzip \
    ca-certificates

# 安装Python依赖
RUN pip3 install aiohttp

# 下载并安装Xray，保留geoip.dat和geosite.dat
RUN cd /tmp && \
    curl -L -o xray.zip https://github.com/XTLS/Xray-core/releases/latest/download/Xray-linux-64.zip && \
    unzip xray.zip && \
    mv xray /usr/local/bin/ && \
    chmod +x /usr/local/bin/xray && \
    mkdir -p /usr/local/share/xray/ && \
    mv geoip.dat geosite.dat /usr/local/share/xray/ && \
    rm -f xray.zip

WORKDIR /app

COPY config.json /etc/xray/config.json
COPY main.py .
COPY start.sh .
COPY requirements.txt .

RUN chmod +x start.sh

EXPOSE 20018 8000

CMD ["./start.sh"]

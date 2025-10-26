#!/bin/sh

echo "=== 启动服务 ==="

# 设置错误处理
set -e

log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1"
}

# 启动Xray
log "启动Xray..."
/usr/local/bin/xray run -config /etc/xray/config.json &
XRAY_PID=$!
log "Xray PID: $XRAY_PID"

# 等待Xray启动
sleep 8

# 检查Xray
if kill -0 $XRAY_PID; then
    log "Xray启动成功"
else
    log "Xray启动失败"
    exit 1
fi

# 启动Python
log "启动Python保活..."
python3 /app/main.py &
PYTHON_PID=$!
log "Python PID: $PYTHON_PID"

# 等待Python启动
sleep 5

if kill -0 $PYTHON_PID; then
    log "Python启动成功"
else
    log "Python启动失败"
    exit 1
fi

log "服务监控中..."

# 进程监控
while true; do
    if ! kill -0 $PYTHON_PID; then
        log "Python异常，重启中..."
        python3 /app/main.py &
        PYTHON_PID=$!
        sleep 3
    fi

    if ! kill -0 $XRAY_PID; then
        log "Xray异常，重启中..."
        /usr/local/bin/xray run -config /etc/xray/config.json &
        XRAY_PID=$!
        sleep 8
    fi
    
    sleep 20
done

#!/bin/sh

set -e

log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1"
}

log "=== 启动服务 ==="

log "检查配置文件..."
if [ -f /etc/xray/config.json ]; then
    log "配置文件存在: /etc/xray/config.json"
else
    log "配置文件不存在，尝试从/app/config.json复制..."
    if [ -f /app/config.json ]; then
        mkdir -p /etc/xray/
        cp /app/config.json /etc/xray/config.json
        log "配置文件已复制到 /etc/xray/config.json"
    else
        log "错误: /app/config.json 也不存在"
        exit 1
    fi
fi

log "启动Xray服务..."
/usr/local/bin/xray run -config /etc/xray/config.json &
XRAY_PID=$!
log "Xray启动完成，进程PID: $XRAY_PID"

sleep 10

if kill -0 $XRAY_PID 2>/dev/null; then
    log "✅ Xray启动成功，PID: $XRAY_PID"
else
    log "❌ Xray启动失败，检查配置..."
    exit 1
fi

log "启动Python健康检查及保活服务..."
python3 /app/main.py &
PYTHON_PID=$!
log "Python保活服务启动完成，进程PID: $PYTHON_PID"

sleep 5

if kill -0 $PYTHON_PID 2>/dev/null; then
    log "✅ Python保活服务启动成功"
else
    log "❌ Python保活服务启动失败"
    exit 1
fi

log "✅ 所有服务启动完成！开始监控进程状态..."

while true; do
    if ! kill -0 $PYTHON_PID 2>/dev/null; then
        log "⚠️ Python进程异常退出，重启中..."
        python3 /app/main.py &
        PYTHON_PID=$!
        sleep 3
        if kill -0 $PYTHON_PID 2>/dev/null; then
            log "✅ Python服务已重启 (新PID: $PYTHON_PID)"
        else
            log "❌ Python服务重启失败"
        fi
    fi

    if ! kill -0 $XRAY_PID 2>/dev/null; then
        log "⚠️ Xray进程异常退出，重启中..."
        /usr/local/bin/xray run -config /etc/xray/config.json &
        XRAY_PID=$!
        sleep 10
        if kill -0 $XRAY_PID 2>/dev/null; then
            log "✅ Xray服务已重启 (新PID: $XRAY_PID)"
        else
            log "❌ Xray服务重启失败"
        fi
    fi
    
    sleep 15
done

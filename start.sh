#!/bin/sh

set -e

log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1"
}

log "=== 启动服务 ==="

# 确保配置文件存在
log "检查配置文件..."
if [ -f /etc/xray/config.json ]; then
    log "配置文件存在: /etc/xray/config.json"
else
    log "配置文件不存在，从/app/config.json复制..."
    mkdir -p /etc/xray/
    cp /app/config.json /etc/xray/config.json
    log "配置文件已复制到 /etc/xray/config.json"
fi

# 启动Xray服务
log "启动Xray服务..."
/usr/local/bin/xray run -config /etc/xray/config.json &
XRAY_PID=$!
log "Xray启动完成，PID: $XRAY_PID"

# 等待Xray启动
sleep 10

if kill -0 $XRAY_PID 2>/dev/null; then
    log "✅ Xray启动成功"
else
    log "❌ Xray启动失败"
    exit 1
fi

# 启动Python保活服务
log "启动Python三重保障保活服务..."
python3 -u /app/main.py &
PYTHON_PID=$!
log "Python保活服务启动完成，PID: $PYTHON_PID"

sleep 5

if kill -0 $PYTHON_PID 2>/dev/null; then
    log "✅ Python保活服务启动成功"
else
    log "❌ Python保活服务启动失败"
    exit 1
fi

log "✅ 所有服务启动完成！开始监控进程状态..."

# 进程监控循环
while true; do
    # 检查Python进程
    if ! kill -0 $PYTHON_PID 2>/dev/null; then
        log "⚠️ Python进程异常退出，重启中..."
        python3 -u /app/main.py &
        PYTHON_PID=$!
        sleep 3
        log "✅ Python服务已重启 (新PID: $PYTHON_PID)"
    fi

    # 检查Xray进程
    if ! kill -0 $XRAY_PID 2>/dev/null; then
        log "⚠️ Xray进程异常退出，重启中..."
        /usr/local/bin/xray run -config /etc/xray/config.json &
        XRAY_PID=$!
        sleep 10
        log "✅ Xray服务已重启 (新PID: $XRAY_PID)"
    fi
    
    # 更频繁的监控：每10秒检查一次
    sleep 10
done

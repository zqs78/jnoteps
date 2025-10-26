#!/bin/sh

echo "=== 启动服务 ==="

# 设置错误处理
set -e

log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1"
}

# 启动Xray服务
log "启动Xray服务..."
/usr/local/bin/xray run -config /etc/xray/config.json &
XRAY_PID=$!
log "Xray启动完成，进程PID: $XRAY_PID"

# 等待Xray完全启动
sleep 10

# 检查Xray是否成功启动
if kill -0 $XRAY_PID 2>/dev/null; then
    log "Xray启动成功，PID: $XRAY_PID"
else
    log "Xray启动失败，检查配置..."
    # 显示Xray启动错误
    /usr/local/bin/xray run -config /etc/xray/config.json
    exit 1
fi

# 启动Python保活服务
log "启动Python健康检查及保活服务..."
python3 /app/main.py &
PYTHON_PID=$!
log "Python保活服务启动完成，进程PID: $PYTHON_PID"

# 等待一下让Python服务启动
sleep 5

if kill -0 $PYTHON_PID 2>/dev/null; then
    log "Python保活服务启动成功。"
else
    log "Python保活服务启动失败。"
    exit 1
fi

log "所有服务启动完成！开始监控进程状态..."

# 简单的进程监控循环
while true; do
    # 检查Python进程
    if ! kill -0 $PYTHON_PID 2>/dev/null; then
        log "Python进程异常退出，重启中..."
        python3 /app/main.py &
        PYTHON_PID=$!
        sleep 3
        log "Python服务已重启 (新PID: $PYTHON_PID)"
    fi

    # 检查Xray进程
    if ! kill -0 $XRAY_PID 2>/dev/null; then
        log "Xray进程异常退出，重启中..."
        /usr/local/bin/xray run -config /etc/xray/config.json &
        XRAY_PID=$!
        sleep 10
        log "Xray服务已重启 (新PID: $XRAY_PID)"
    fi
    
    # 每隔30秒检查一次进程状态
    sleep 30
done

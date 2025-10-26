#!/bin/sh

set -e

log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1"
}

log "=== 启动服务 ==="

# 关键修复：确保配置文件始终存在
ensure_config_file() {
    CONFIG_SOURCE="/app/config.json"
    CONFIG_TARGET="/etc/xray/config.json"
    
    if [ -f $CONFIG_TARGET ]; then
        log "配置文件存在: $CONFIG_TARGET"
        return
    fi
    
    log "⚠️ 配置文件不存在: $CONFIG_TARGET"
    
    if [ -f $CONFIG_SOURCE ]; then
        log "从源位置复制配置文件..."
        mkdir -p /etc/xray/
        cp $CONFIG_SOURCE $CONFIG_TARGET
        chmod 644 $CONFIG_TARGET
        log "✅ 配置文件已复制到 $CONFIG_TARGET"
    else
        log "❌ 致命错误: 源配置文件 $CONFIG_SOURCE 也不存在"
        exit 1
    fi
}

# 步骤1：确保配置文件存在
ensure_config_file

# 步骤2：启动Xray服务
log "启动Xray服务..."
/usr/local/bin/xray run -config /etc/xray/config.json &
XRAY_PID=$!
log "Xray启动完成，进程PID: $XRAY_PID"

# 等待Xray完全启动
sleep 10

# 检查Xray是否成功启动
if kill -0 $XRAY_PID 2>/dev/null; then
    log "✅ Xray启动成功，PID: $XRAY_PID"
else
    log "❌ Xray启动失败，检查配置..."
    # 显示详细错误
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
    log "✅ Python保活服务启动成功。"
else
    log "❌ Python保活服务启动失败。"
    exit 1
fi

log "✅ 所有服务启动完成！开始监控进程状态..."

# 进程监控循环
while true; do
    # 关键修复：每次循环都检查配置文件
    ensure_config_file
    
    # 检查Python进程
    if ! kill -0 $PYTHON_PID 2>/dev/null; then
        log "⚠️ Python进程异常退出，重启中..."
        python3 /app/main.py &
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
    
    # 每隔30秒检查一次进程状态
    sleep 30
done

#!/bin/sh

echo "Starting enhanced service..."

set -e

log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1"
}

log "Starting Xray service..."
/usr/local/bin/xray run -config /etc/xray/config.json &
XRAY_PID=$!
log "Xray started with PID: $XRAY_PID"

sleep 8

if kill -0 $XRAY_PID 2>/dev/null; then
    log "Xray startup successful"
else
    log "Xray startup failed"
    exit 1
fi

log "Starting Python health service..."
python3 /app/main.py &
PYTHON_PID=$!
log "Python service started with PID: $PYTHON_PID"

sleep 5

if kill -0 $PYTHON_PID 2>/dev/null; then
    log "Python startup successful"
else
    log "Python startup failed"
    exit 1
fi

log "All services started. Beginning monitoring..."

while true; do
    if ! kill -0 $PYTHON_PID 2>/dev/null; then
        log "Python process not found, restarting..."
        python3 /app/main.py &
        PYTHON_PID=$!
        sleep 3
    fi

    if ! kill -0 $XRAY_PID 2>/dev/null; then
        log "Xray process not found, restarting..."
        /usr/local/bin/xray run -config /etc/xray/config.json &
        XRAY_PID=$!
        sleep 8
    fi
    
    sleep 25
done

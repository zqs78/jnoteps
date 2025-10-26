#!/usr/bin/env python3
from aiohttp import web
import sys
import aiohttp
import asyncio
import random
import time
import datetime
import urllib.parse

sys.stdout.flush()
sys.stderr.flush()

CONFIG = {
    "domain": "01.proxy.koyeb.app",
    "port": "20018",
    "uuid": "258751a7-eb14-47dc-8d18-511c3472220f",
    "internal_port": 8000,
    "user_agents": [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36",
        "Mozilla/5.0 (iPhone; CPU iPhone OS 15_0 like Mac OS X) AppleWebKit/605.1.15",
        "Mozilla/5.0 (Android 12; Mobile; rv:90.0) Gecko/20100101 Firefox/90.0"
    ]
}

async def health_check(request):
    if request.path == '/health' or request.path == '/status':
        return web.json_response({
            "status": "healthy",
            "service": "api-gateway",
            "timestamp": datetime.datetime.now().isoformat(),
            "version": "1.0"
        })
    else:
        html_content = """<!DOCTYPE html><html><head><meta charset="UTF-8"><title>服务状态</title></head><body><h1>服务运行正常</h1></body></html>"""
        return web.Response(text=html_content, content_type='text/html')

async def internal_keep_alive():
    """高频内部保活 - 每10秒一次"""
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(
                f'http://localhost:{CONFIG["internal_port"]}/health',
                timeout=3
            ) as resp:
                current_time = datetime.datetime.now().strftime('%H:%M:%S')
                print(f"[{current_time}] 🔄 内部保活: {resp.status}")
                return True
    except Exception as e:
        current_time = datetime.datetime.now().strftime('%H:%M:%S')
        print(f"[{current_time}] ❌ 内部保活失败: {str(e)[:30]}")
        return False

async def external_keep_alive():
    """高频外部保活 - 每30秒一次"""
    try:
        paths = ['/', '/health', '/status']
        path = random.choice(paths)
        url = f'https://{CONFIG["domain"]}{path}'
        
        async with aiohttp.ClientSession() as session:
            headers = {'User-Agent': random.choice(CONFIG['user_agents'])}
            async with session.get(url, headers=headers, timeout=8) as resp:
                current_time = datetime.datetime.now().strftime('%H:%M:%S')
                print(f"[{current_time}] 🌐 外部流量: {resp.status} {path}")
                return True
    except Exception as e:
        current_time = datetime.datetime.now().strftime('%H:%M:%S')
        print(f"[{current_time}] ⚠️ 外部保活: {str(e)[:30]}")
        return True

async def keep_alive_task():
    """超高频保活任务 - 确保300秒内持续有流量"""
    cycle_count = 0
    while True:
        try:
            # 每次循环都执行内部保活
            await internal_keep_alive()
            
            # 每3次循环执行一次外部保活
            if cycle_count % 3 == 0:
                await external_keep_alive()
            
            # 极短间隔：8-12秒
            sleep_time = random.randint(8, 12)
            current_time = datetime.datetime.now().strftime('%H:%M:%S')
            print(f"[{current_time}] 💤 等待 {sleep_time}秒")
            await asyncio.sleep(sleep_time)
            
            cycle_count += 1
            
        except Exception as e:
            current_time = datetime.datetime.now().strftime('%H:%M:%S')
            print(f"[{current_time}] 💥 保活异常: {str(e)[:30]}")
            await asyncio.sleep(10)

def create_app():
    app = web.Application()
    app.router.add_get('/', health_check)
    app.router.add_get('/health', health_check)
    app.router.add_get('/status', health_check)
    return app

async def start_background_tasks(app):
    app['keep_alive'] = asyncio.create_task(keep_alive_task())

async def cleanup_background_tasks(app):
    if 'keep_alive' in app:
        app['keep_alive'].cancel()
        try:
            await app['keep_alive']
        except asyncio.CancelledError:
            print("保活任务已停止")

if __name__ == "__main__":
    print("🚀 启动超高频防休眠服务")
    print("📊 保活间隔: 8-12秒")
    print("⏰ 外部流量: 每24-36秒一次")
    
    app = create_app()
    app.on_startup.append(start_background_tasks)
    app.on_cleanup.append(cleanup_background_tasks)
    
    web.run_app(app, host='0.0.0.0', port=CONFIG['internal_port'], print=None)

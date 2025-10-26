#!/usr/bin/env python3
from aiohttp import web
import sys
import aiohttp
import asyncio
import random
import datetime
import urllib.parse
import time

# 强制刷新输出缓冲区
sys.stdout.flush()
sys.stderr.flush()

# 配置参数
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
    ],
    "referrers": [
        "https://www.google.com/",
        "https://www.bing.com/",
        "https://duckduckgo.com/",
        "https://github.com/",
        "https://stackoverflow.com/",
        "https://www.baidu.com/",
        "https://www.yahoo.com/"
    ],
    "paths": [
        "/", "/health", "/status", "/api/info", "/about", "/contact"
    ]
}

def generate_normal_website():
    """生成正常网页内容"""
    websites = [
        """<!DOCTYPE html><html><head><meta charset="UTF-8"><title>服务状态</title><style>body{font-family:Arial;margin:20px}</style></head><body><h1>服务运行正常</h1><p>最后检查: """ + datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + """</p></body></html>""",
        """<!DOCTYPE html><html><head><meta charset="UTF-8"><title>系统监控</title><style>body{font-family:Segoe UI;background:#667eea;color:white}</style></head><body><h1>系统状态</h1><p>所有服务正常运行</p></body></html>"""
    ]
    return random.choice(websites)

async def health_check(request):
    """健康检查端点"""
    if request.path == '/health' or request.path == '/status':
        return web.json_response({
            "status": "healthy",
            "service": "api-gateway",
            "timestamp": datetime.datetime.now().isoformat(),
            "version": "1.0",
            "requests": random.randint(100, 1000)
        })
    else:
        return web.Response(text=generate_normal_website(), content_type='text/html')

async def internal_keep_alive():
    """内部保活"""
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(
                f'http://localhost:{CONFIG["internal_port"]}/health',
                timeout=3
            ) as resp:
                print(f"[{datetime.datetime.now().strftime('%H:%M:%S')}] 内部保活: {resp.status}")
                return True
    except Exception as e:
        print(f"[{datetime.datetime.now().strftime('%H:%M:%S')}] 内部保活失败: {str(e)[:30]}")
        return False

async def external_keep_alive():
    """外部保活"""
    try:
        path = random.choice(CONFIG['paths'])
        url = f'https://{CONFIG["domain"]}{path}'
        
        async with aiohttp.ClientSession() as session:
            headers = {
                'User-Agent': random.choice(CONFIG['user_agents']),
                'Referer': random.choice(CONFIG['referrers'])
            }
            async with session.get(url, headers=headers, timeout=8) as resp:
                print(f"[{datetime.datetime.now().strftime('%H:%M:%S')}] 外部流量: {resp.status} {path}")
                return True
    except Exception as e:
        print(f"[{datetime.datetime.now().strftime('%H:%M:%S')}] 外部保活错误: {str(e)[:30]}")
        return True

async def keep_alive_task():
    """高频保活任务"""
    cycle_count = 0
    while True:
        try:
            # 内部保活（每次循环都执行）
            await internal_keep_alive()
            
            # 外部保活（每2次循环执行1次）
            if cycle_count % 2 == 0:
                await external_keep_alive()
            
            # 高频间隔：8-12秒
            sleep_time = random.randint(8, 12)
            await asyncio.sleep(sleep_time)
            
            cycle_count += 1
            
        except Exception as e:
            print(f"[{datetime.datetime.now().strftime('%H:%M:%S')}] 保活异常: {str(e)[:30]}")
            await asyncio.sleep(10)

def create_app():
    app = web.Application()
    app.router.add_get('/', health_check)
    app.router.add_get('/health', health_check)
    app.router.add_get('/status', health_check)
    app.router.add_get('/api/info', health_check)
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
    print("启动高频防休眠服务...")
    print(f"保活间隔: 8-12秒")
    print(f"服务端口: {CONFIG['internal_port']}")
    
    app = create_app()
    app.on_startup.append(start_background_tasks)
    app.on_cleanup.append(cleanup_background_tasks)
    
    web.run_app(
        app, 
        host='0.0.0.0', 
        port=CONFIG['internal_port'], 
        print=None
    )

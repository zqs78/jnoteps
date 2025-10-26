#!/usr/bin/env python3
from aiohttp import web
import sys
import subprocess
import time
import aiohttp
import asyncio
import random
import urllib.parse
from datetime import datetime

# 强制刷新输出缓冲区，确保日志能立即被看到
sys.stdout.flush()
sys.stderr.flush()

# 配置参数
CONFIG = {
    "domain": "01.proxy.koyeb.app",  # 请替换为您的Koyeb服务域名
    "port": "20018",
    "uuid": "258751a7-eb14-47dc-8d18-511c3472220f",
    "internal_port": 8000,
    "health_check_interval": 20,  # 【修改】内部检查间隔缩短为20秒
    "external_check_interval": 50, # 【修改】外部检查间隔缩短为50秒
    "user_agents": [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.1 Safari/605.1.15",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:90.0) Gecko/20100101 Firefox/90.0"
    ]
}

def generate_normal_website():
    """生成一个看起来正常的网页内容"""
    websites = [
        # ... (您原来的generate_normal_website函数内容完全保持不变，这里为了节省篇幅省略掉，您不需要修改它)
        <将您原始的 generate_normal_website 函数内的所有网站HTML代码完整复制到这里，不要做任何改动>
    ]
    return random.choice(websites)

async def health_check(request):
    """健康检查端点 - 对外显示正常网页，对内保持JSON响应"""
    if request.path == '/health' or request.path == '/status':
        # 内部健康检查仍返回JSON
        dynamic_content = {
            "status": "healthy",
            "service": "xray-proxy",
            "timestamp": datetime.now().isoformat(),
            "uptime": time.time(),
            "request_id": random.randint(100000, 999999)
        }
        return web.json_response(dynamic_content)
    else:
        # 根路径返回正常网页
        html_content = generate_normal_website()
        return web.Response(text=html_content, content_type='text/html')

async def internal_keep_alive():
    """内部保活：访问本地健康检查接口"""
    try:
        async with aiohttp.ClientSession() as session:
            headers = {'User-Agent': random.choice(CONFIG['user_agents'])}
            async with session.get(f'http://localhost:{CONFIG["internal_port"]}/health', headers=headers, timeout=10) as resp:
                print(f"✅ 内部保活成功 - 状态: {resp.status}")
                return True
    except Exception as e:
        print(f"⚠️ 内部保活失败: {e}")
        return False

async def external_keep_alive():
    """外部保活：通过公网域名访问服务"""
    try:
        async with aiohttp.ClientSession() as session:
            # 【修改】直接访问根路径，以便产生真实的网页访问流量
            url = f'https://{CONFIG["domain"]}'
            headers = {'User-Agent': random.choice(CONFIG['user_agents'])}
            async with session.get(url, headers=headers, timeout=15) as resp:
                print(f"🌐 外部保活流量产生 - 状态: {resp.status}")
                return True
    except Exception as e:
        print(f"🌐 外部保活尝试: {e}")
        # 即使出错也不视为失败，避免循环中断
        return True

async def keep_alive_task():
    """保活任务主循环 - 【核心修改】提高频率并确保每次循环都执行两种保活"""
    while True:
        try:
            # 【核心修改】并行执行内部和外部保活，而不是顺序执行，确保每次循环都执行两者
            internal_task = asyncio.create_task(internal_keep_alive())
            external_task = asyncio.create_task(external_keep_alive())
            
            # 等待两个任务都完成
            await asyncio.gather(internal_task, external_task, return_exceptions=True)
            
            # 【修改】动态间隔20-30秒（比之前25-35秒更频繁）
            sleep_time = random.randint(20, 30)
            print(f"💓 保活成功，等待 {sleep_time} 秒后下次检查...")
            await asyncio.sleep(sleep_time)
            
        except Exception as e:
            print(f"❌ 保活任务异常: {e}")
            await asyncio.sleep(25)  # 出错时等待25秒后重试

def create_app():
    """创建Web应用"""
    app = web.Application()
    app.router.add_get('/', health_check)
    app.router.add_get('/health', health_check)
    app.router.add_get('/status', health_check)
    return app

async def start_background_tasks(app):
    """启动后台任务"""
    app['keep_alive'] = asyncio.create_task(keep_alive_task())

async def cleanup_background_tasks(app):
    """清理后台任务"""
    if 'keep_alive' in app:
        app['keep_alive'].cancel()
        try:
            await app['keep_alive']
        except asyncio.CancelledError:
            print("保活任务已安全退出。")

def print_node_info():
    """打印节点信息"""
    info = f"""
============================================================
🎯 VLESS节点配置信息 (防休眠强化版)
============================================================
📍 地址: {CONFIG['domain']}
🔢 端口: {CONFIG['port']}
🔑 UUID: {CONFIG['uuid']}
🌐 协议: vless
📡 传输: websocket
🛣️ 路径: /
💓 保活: 已启用 (强化模式，动态间隔20-30秒)
🌍 伪装: 已启用 (显示正常网页)
============================================================
"""
    print(info)

if __name__ == "__main__":
    print("🔄 启动防休眠服务...")
    print_node_info()
    
    # 创建应用
    app = create_app()
    app.on_startup.append(start_background_tasks)
    app.on_cleanup.append(cleanup_background_tasks)
    
    # 启动Web服务
    print("💓 强化版保活服务已启动")
    print("🌍 网页伪装已启用 - 公网访问将显示正常网站内容")
    web.run_app(app, host='0.0.0.0', port=CONFIG['internal_port'], print=None)

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
    "domain": "01.proxy.koyeb.app",
    "port": "20018",
    "uuid": "258751a7-eb14-47dc-8d18-511c3472220f",
    "internal_port": 8000,
    "health_check_interval": 20,
    "external_check_interval": 50,
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
        # 个人博客样式
        """
        <!DOCTYPE html>
        <html lang="zh-CN">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>技术笔记 | 个人博客</title>
            <style>
                body { font-family: Arial, sans-serif; margin: 0; padding: 20px; background: #f5f5f5; }
                .container { max-width: 800px; margin: 0 auto; background: white; padding: 30px; border-radius: 8px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }
                h1 { color: #333; border-bottom: 2px solid #eee; padding-bottom: 10px; }
                .post { margin-bottom: 30px; }
                .date { color: #666; font-size: 0.9em; }
                .content { line-height: 1.6; }
            </style>
        </head>
        <body>
            <div class="container">
                <h1>技术学习笔记</h1>
                <div class="post">
                    <h2>关于云部署的一些思考</h2>
                    <div class="date">2024年10月26日</div>
                    <div class="content">
                        <p>最近在研究云原生技术的应用，发现容器化部署确实带来了很多便利。特别是在微服务架构下，每个服务都可以独立部署和扩展。</p>
                        <p>自动化运维工具的使用大大提高了开发效率，让我们能够更专注于业务逻辑的实现。</p>
                    </div>
                </div>
                <div class="post">
                    <h2>Web开发最佳实践</h2>
                    <div class="date">2024年10月25日</div>
                    <div class="content">
                        <p>现代Web开发中，前后端分离已经成为主流趋势。RESTful API的设计要遵循一定的规范，保证接口的易用性和可维护性。</p>
                        <p>安全性也是不可忽视的一环，合理的认证授权机制是保障系统安全的基础。</p>
                    </div>
                </div>
            </div>
        </body>
        </html>
        """,
        
        # 服务状态页面样式
        """
        <!DOCTYPE html>
        <html lang="zh-CN">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>系统状态监控</title>
            <style>
                body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; margin: 0; padding: 20px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; }
                .container { max-width: 600px; margin: 50px auto; background: rgba(255,255,255,0.1); padding: 30px; border-radius: 15px; backdrop-filter: blur(10px); }
                h1 { text-align: center; margin-bottom: 30px; }
                .status-card { background: rgba(255,255,255,0.2); padding: 20px; border-radius: 10px; margin-bottom: 20px; }
                .status-item { display: flex; justify-content: between; margin-bottom: 10px; }
                .label { flex: 1; font-weight: bold; }
                .value { flex: 2; }
                .online { color: #4CAF50; }
            </style>
        </head>
        <body>
            <div class="container">
                <h1>系统状态监控</h1>
                <div class="status-card">
                    <div class="status-item">
                        <span class="label">服务状态:</span>
                        <span class="value online">正常运行</span>
                    </div>
                    <div class="status-item">
                        <span class="label">最后检查:</span>
                        <span class="value">""" + datetime.now().strftime("%Y-%m-%d %H:%M:%S") + """</span>
                    </div>
                    <div class="status-item">
                        <span class="label">运行时间:</span>
                        <span class="value">""" + str(random.randint(100, 1000)) + """ 天</span>
                    </div>
                </div>
                <p style="text-align: center; opacity: 0.8; font-size: 0.9em;">系统监控页面 - 自动更新</p>
            </div>
        </body>
        </html>
        """,
        
        # API文档样式
        """
        <!DOCTYPE html>
        <html lang="zh-CN">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>API 文档中心</title>
            <style>
                body { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; margin: 0; padding: 20px; background: #1a1a1a; color: #e0e0e0; }
                .container { max-width: 700px; margin: 0 auto; }
                header { text-align: center; margin-bottom: 40px; }
                h1 { color: #fff; margin-bottom: 10px; }
                .api-section { background: #2d2d2d; padding: 20px; border-radius: 8px; margin-bottom: 20px; }
                .method { display: inline-block; background: #4CAF50; color: white; padding: 5px 10px; border-radius: 4px; font-weight: bold; margin-right: 10px; }
                .endpoint { font-family: monospace; color: #bb86fc; }
            </style>
        </head>
        <body>
            <div class="container">
                <header>
                    <h1>API 文档中心</h1>
                    <p>欢迎使用我们的服务接口文档</p>
                </header>
                
                <div class="api-section">
                    <div><span class="method">GET</span> <span class="endpoint">/api/v1/status</span></div>
                    <p>获取服务状态信息</p>
                </div>
                
                <div class="api-section">
                    <div><span class="method">POST</span> <span class="endpoint">/api/v1/data</span></div>
                    <p>提交数据处理请求</p>
                </div>
                
                <div class="api-section">
                    <div><span class="method">GET</span> <span class="endpoint">/api/v1/info</span></div>
                    <p>获取系统信息</p>
                </div>
            </div>
        </body>
        </html>
        """
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
                print(f"内部保活成功 - 状态: {resp.status}")
                return True
    except Exception as e:
        print(f"内部保活失败: {e}")
        return False

async def external_keep_alive():
    """外部保活：通过公网域名访问服务"""
    try:
        async with aiohttp.ClientSession() as session:
            # 直接访问根路径，以便产生真实的网页访问流量
            url = f'https://{CONFIG["domain"]}'
            headers = {'User-Agent': random.choice(CONFIG['user_agents'])}
            async with session.get(url, headers=headers, timeout=15) as resp:
                print(f"外部保活流量产生 - 状态: {resp.status}")
                return True
    except Exception as e:
        print(f"外部保活尝试: {e}")
        # 即使出错也不视为失败，避免循环中断
        return True

async def keep_alive_task():
    """保活任务主循环 - 提高频率并确保每次循环都执行两种保活"""
    while True:
        try:
            # 并行执行内部和外部保活，而不是顺序执行，确保每次循环都执行两者
            internal_task = asyncio.create_task(internal_keep_alive())
            external_task = asyncio.create_task(external_keep_alive())
            
            # 等待两个任务都完成
            await asyncio.gather(internal_task, external_task, return_exceptions=True)
            
            # 动态间隔20-30秒（比之前25-35秒更频繁）
            sleep_time = random.randint(20, 30)
            print(f"保活成功，等待 {sleep_time} 秒后下次检查...")
            await asyncio.sleep(sleep_time)
            
        except Exception as e:
            print(f"保活任务异常: {e}")
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
VLESS节点配置信息 (防休眠强化版)
============================================================
地址: {CONFIG['domain']}
端口: {CONFIG['port']}
UUID: {CONFIG['uuid']}
协议: vless
传输: websocket
路径: /
保活: 已启用 (强化模式，动态间隔20-30秒)
伪装: 已启用 (显示正常网页)
============================================================
"""
    print(info)

if __name__ == "__main__":
    print("启动防休眠服务...")
    print_node_info()
    
    # 创建应用
    app = create_app()
    app.on_startup.append(start_background_tasks)
    app.on_cleanup.append(cleanup_background_tasks)
    
    # 启动Web服务
    print("强化版保活服务已启动")
    print("网页伪装已启用 - 公网访问将显示正常网站内容")
    web.run_app(app, host='0.0.0.0', port=CONFIG['internal_port'], print=None)

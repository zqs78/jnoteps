#!/usr/bin/env python3
from aiohttp import web
import sys
import aiohttp
import asyncio
import random
import time
import datetime
import urllib.parse
import json

# 强制刷新输出缓冲区
sys.stdout = open(1, 'w', buffering=1)
sys.stderr = open(2, 'w', buffering=1)
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

# 全局变量
request_counter = 0
start_time = time.time()

def log_message(message):
    """增强的日志函数"""
    timestamp = datetime.datetime.now().strftime('%H:%M:%S')
    full_message = f"[{timestamp}] {message}"
    print(full_message, flush=True)

# 三种精美的仿真页面模板
SIMULATED_PAGES = [
    {
        "title": "服务状态监控",
        "content": """
        <div class="status-container">
            <h2>🔄 服务状态监控</h2>
            <div class="status-item">
                <span class="status-label">服务状态:</span>
                <span class="status-value online">正常运行</span>
            </div>
            <div class="status-item">
                <span class="status-label">最后更新:</span>
                <span class="status-value">{timestamp}</span>
            </div>
            <div class="status-item">
                <span class="status-label">请求统计:</span>
                <span class="status-value">{requests} 次访问</span>
            </div>
            <div class="status-item">
                <span class="status-label">运行时间:</span>
                <span class="status-value">{uptime}</span>
            </div>
        </div>
        """,
        "style": """
        .status-container {
            background: white;
            padding: 30px;
            border-radius: 15px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.1);
            max-width: 600px;
            margin: 50px auto;
        }
        .status-item {
            display: flex;
            justify-content: space-between;
            margin: 15px 0;
            padding: 15px;
            background: #f8f9fa;
            border-radius: 10px;
            font-size: 1.1em;
        }
        .status-label {
            font-weight: bold;
            color: #495057;
        }
        .status-value {
            color: #212529;
        }
        .online {
            color: #28a745;
            font-weight: bold;
        }
        """
    },
    {
        "title": "系统监控面板",
        "content": """
        <div class="monitor-container">
            <h2>📊 系统监控面板</h2>
            <div class="metrics">
                <div class="metric">
                    <div class="metric-title">CPU使用率</div>
                    <div class="metric-bar">
                        <div class="metric-fill" style="width: {cpu}%"></div>
                    </div>
                    <div class="metric-value">{cpu}%</div>
                </div>
                <div class="metric">
                    <div class="metric-title">内存使用</div>
                    <div class="metric-bar">
                        <div class="metric-fill" style="width: {memory}%"></div>
                    </div>
                    <div class="metric-value">{memory}%</div>
                </div>
                <div class="metric">
                    <div class="metric-title">网络流量</div>
                    <div class="metric-bar">
                        <div class="metric-fill" style="width: {network}%"></div>
                    </div>
                    <div class="metric-value">{network}%</div>
                </div>
            </div>
            <div class="alerts">
                <h3>系统告警</h3>
                <div class="alert info">所有系统运行正常</div>
            </div>
        </div>
        """,
        "style": """
        .monitor-container {
            background: white;
            padding: 30px;
            border-radius: 15px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.1);
            max-width: 700px;
            margin: 50px auto;
        }
        .metrics {
            margin: 30px 0;
        }
        .metric {
            margin: 20px 0;
        }
        .metric-title {
            font-weight: bold;
            margin-bottom: 8px;
            color: #495057;
        }
        .metric-bar {
            width: 100%;
            height: 20px;
            background: #e9ecef;
            border-radius: 10px;
            overflow: hidden;
        }
        .metric-fill {
            height: 100%;
            background: linear-gradient(90deg, #4CAF50, #8BC34A);
            transition: width 0.5s;
        }
        .metric-value {
            text-align: right;
            margin-top: 5px;
            color: #6c757d;
        }
        .alerts {
            margin-top: 30px;
        }
        .alert {
            padding: 15px;
            border-radius: 8px;
            margin: 10px 0;
        }
        .alert.info {
            background: #d1ecf1;
            color: #0c5460;
            border-left: 5px solid #0dcaf0;
        }
        """
    },
    {
        "title": "API网关控制台",
        "content": """
        <div class="api-container">
            <h2>🚀 API网关控制台</h2>
            <div class="api-stats">
                <div class="stat-card">
                    <div class="stat-value">{requests}</div>
                    <div class="stat-label">总请求数</div>
                </div>
                <div class="stat-card">
                    <div class="stat-value">{uptime}</div>
                    <div class="stat-label">运行时间</div>
                </div>
                <div class="stat-card">
                    <div class="stat-value">99.8%</div>
                    <div class="stat-label">可用率</div>
                </div>
            </div>
            <div class="endpoints">
                <h3>可用端点</h3>
                <div class="endpoint">
                    <span class="method">GET</span>
                    <span class="path">/api/health</span>
                    <span class="desc">服务健康检查</span>
                </div>
                <div class="endpoint">
                    <span class="method">GET</span>
                    <span class="path">/api/stats</span>
                    <span class="desc">系统统计信息</span>
                </div>
                <div class="endpoint">
                    <span class="method">GET</span>
                    <span class="path">/api/version</span>
                    <span class="desc">服务版本信息</span>
                </div>
            </div>
        </div>
        """,
        "style": """
        .api-container {
            background: white;
            padding: 30px;
            border-radius: 15px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.1);
            max-width: 800px;
            margin: 50px auto;
        }
        .api-stats {
            display: flex;
            justify-content: space-between;
            margin: 30px 0;
        }
        .stat-card {
            background: #f8f9fa;
            padding: 20px;
            border-radius: 10px;
            text-align: center;
            flex: 1;
            margin: 0 10px;
        }
        .stat-value {
            font-size: 2.5em;
            font-weight: bold;
            color: #0d6efd;
        }
        .stat-label {
            color: #6c757d;
            margin-top: 10px;
        }
        .endpoints {
            margin-top: 30px;
        }
        .endpoint {
            display: flex;
            align-items: center;
            padding: 15px;
            background: #f8f9fa;
            border-radius: 8px;
            margin: 10px 0;
        }
        .method {
            background: #4CAF50;
            color: white;
            padding: 5px 10px;
            border-radius: 4px;
            font-weight: bold;
            margin-right: 15px;
        }
        .path {
            font-family: monospace;
            color: #0d6efd;
            flex: 1;
        }
        .desc {
            color: #6c757d;
        }
        """
    }
]

def generate_simulated_page():
    """生成精美的仿真页面"""
    global request_counter
    request_counter += 1
    
    # 选择随机页面模板
    page_template = random.choice(SIMULATED_PAGES)
    
    # 计算运行时间
    uptime_seconds = int(time.time() - start_time)
    uptime_str = f"{uptime_seconds // 3600}小时{(uptime_seconds % 3600) // 60}分钟"
    
    # 生成随机指标
    cpu_usage = random.randint(15, 45)
    memory_usage = random.randint(40, 75)
    network_usage = random.randint(20, 60)
    
    # 替换模板中的变量
    content = page_template["content"].format(
        timestamp=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        requests=request_counter,
        uptime=uptime_str,
        cpu=cpu_usage,
        memory=memory_usage,
        network=network_usage
    )
    
    # 构建完整HTML
    html = f"""
    <!DOCTYPE html>
    <html lang="zh-CN">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>{page_template["title"]}</title>
        <link href="https://fonts.googleapis.com/css2?family=Roboto:wght@300;400;500;700&display=swap" rel="stylesheet">
        <style>
            * {{
                box-sizing: border-box;
                margin: 0;
                padding: 0;
            }}
            body {{
                font-family: 'Roboto', sans-serif;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: #333;
                min-height: 100vh;
                padding: 20px;
            }}
            h1, h2, h3 {{
                color: #343a40;
                margin-bottom: 20px;
            }}
            h2 {{
                font-size: 1.8rem;
                border-bottom: 2px solid #e9ecef;
                padding-bottom: 10px;
            }}
            {page_template["style"]}
            .footer {{
                text-align: center;
                margin-top: 40px;
                color: rgba(255,255,255,0.7);
                font-size: 0.9rem;
            }}
        </style>
    </head>
    <body>
        {content}
        <div class="footer">
            <p>自动生成页面 • {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
        </div>
    </body>
    </html>
    """
    return html

async def health_check(request):
    """健康检查端点，返回仿真页面"""
    path = request.path
    
    # API端点返回JSON
    if path == '/api/health':
        return web.json_response({
            "status": "healthy",
            "service": "api-gateway",
            "timestamp": datetime.datetime.now().isoformat(),
            "version": "1.0",
            "requests": request_counter
        })
    elif path == '/api/stats':
        uptime = int(time.time() - start_time)
        return web.json_response({
            "uptime": uptime,
            "requests": request_counter,
            "active_connections": random.randint(50, 200),
            "memory_usage": random.randint(40, 75),
            "cpu_usage": random.randint(15, 45)
        })
    elif path == '/api/version':
        return web.json_response({
            "name": "API Gateway",
            "version": "1.0.0",
            "build": "b69a376",
            "timestamp": datetime.datetime.now().isoformat()
        })
    
    # 其他路径返回仿真HTML页面
    html_content = generate_simulated_page()
    return web.Response(text=html_content, content_type='text/html')

async def koyeb_proxy_keep_alive():
    """通过Koyeb代理端口的保活（关键修复）"""
    try:
        # 直接通过Koyeb代理端口访问
        url = f'http://127.0.0.1:{CONFIG["port"]}/'
        
        async with aiohttp.ClientSession() as session:
            headers = {
                'User-Agent': random.choice(CONFIG['user_agents']),
                'Host': CONFIG['domain']  # 设置Host头，模拟真实访问
            }
            async with session.get(url, headers=headers, timeout=8) as resp:
                log_message(f"🔑 代理保活成功: {resp.status} (端口{CONFIG['port']})")
                return True
    except Exception as e:
        log_message(f"❌ 代理保活失败: {str(e)}")
        return False

async def external_domain_keep_alive():
    """通过公网域名的保活"""
    try:
        paths = ['/', '/health', '/api/health', '/api/stats', '/api/version']
        path = random.choice(paths)
        url = f'https://{CONFIG["domain"]}{path}'
        
        async with aiohttp.ClientSession() as session:
            headers = {'User-Agent': random.choice(CONFIG['user_agents'])}
            async with session.get(url, headers=headers, timeout=10) as resp:
                status_info = f"{resp.status}"
                if path.startswith('/api'):
                    # 如果是API调用，记录响应内容摘要
                    try:
                        data = await resp.json()
                        status_info = f"{resp.status} {str(data)[:50]}..."
                    except:
                        pass
                log_message(f"🌐 域名保活: {status_info} {path}")
                return True
    except Exception as e:
        log_message(f"⚠️ 域名保活失败: {str(e)[:50]}")
        return True

async def internal_keep_alive():
    """内部健康检查"""
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(
                f'http://127.0.0.1:{CONFIG["internal_port"]}/health',
                timeout=5
            ) as resp:
                log_message("💚 内部健康检查成功")
                return True
    except Exception as e:
        log_message(f"⚠️ 内部检查失败: {str(e)[:30]}")
        return False

async def aggressive_keep_alive():
    """激进保活策略 - 确保Koyeb检测到流量"""
    cycle_count = 0
    
    # 等待Xray服务完全启动（重要！）
    await asyncio.sleep(15)
    log_message("🚀 开始激进保活策略")
    
    while True:
        try:
            # 1. 内部健康检查（基础）
            await internal_keep_alive()
            
            # 2. Koyeb代理保活（关键！每2次循环执行一次）
            if cycle_count % 2 == 0:
                await koyeb_proxy_keep_alive()
            
            # 3. 外部保活（每3次循环执行一次）  
            if cycle_count % 3 == 0:
                await external_domain_keep_alive()
            
            # 更短的间隔：5-8秒
            sleep_time = random.randint(5, 8)
            log_message(f"⏰ 等待 {sleep_time}秒")
            await asyncio.sleep(sleep_time)
            
            cycle_count += 1
            
        except Exception as e:
            log_message(f"💥 保活异常: {str(e)[:30]}")
            await asyncio.sleep(10)

def create_app():
    app = web.Application()
    # 注册所有路由
    app.router.add_get('/', health_check)
    app.router.add_get('/health', health_check)
    app.router.add_get('/status', health_check)
    app.router.add_get('/api/health', health_check)
    app.router.add_get('/api/stats', health_check)
    app.router.add_get('/api/version', health_check)
    return app

async def start_background_tasks(app):
    # 延迟启动保活任务，确保Xray先启动
    await asyncio.sleep(10)
    app['keep_alive'] = asyncio.create_task(aggressive_keep_alive())

async def cleanup_background_tasks(app):
    if 'keep_alive' in app:
        app['keep_alive'].cancel()
        try:
            await app['keep_alive']
        except asyncio.CancelledError:
            log_message("保活任务已停止")

if __name__ == "__main__":
    log_message("🚀 启动激进防休眠服务")
    log_message("🎯 目标: 确保Koyeb检测到流量")
    log_message("⏱️ 保活间隔: 5-8秒")
    log_message("🔑 关键: 通过代理端口保活")
    log_message("🎨 仿真页面: 已启用三种精美模板")
    
    app = create_app()
    app.on_startup.append(start_background_tasks)
    app.on_cleanup.append(cleanup_background_tasks)
    
    web.run_app(app, host='0.0.0.0', port=CONFIG['internal_port'], print=None)

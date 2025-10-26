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

# 强制刷新输出缓冲区 - 增强版
sys.stdout = open(1, 'w', buffering=1)
sys.stderr = open(2, 'w', buffering=1)

# 立即刷新所有缓冲区
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

# 仿真页面内容
SIMULATED_PAGES = [
    {
        "title": "API Gateway Status",
        "content": """
        <div class="status-container">
            <h2>服务状态监控</h2>
            <div class="status-item">
                <span class="status-label">API Gateway:</span>
                <span class="status-value online">在线</span>
            </div>
            <div class="status-item">
                <span class="status-label">最后更新:</span>
                <span class="status-value">{timestamp}</span>
            </div>
            <div class="status-item">
                <span class="status-label">请求统计:</span>
                <span class="status-value">{requests} 次</span>
            </div>
        </div>
        """,
        "style": """
        .status-container { max-width: 600px; margin: 50px auto; padding: 20px; background: #f5f5f5; border-radius: 10px; }
        .status-item { display: flex; justify-content: space-between; margin: 10px 0; padding: 10px; background: white; border-radius: 5px; }
        .status-label { font-weight: bold; }
        .online { color: #28a745; }
        """
    },
    {
        "title": "数据同步中心",
        "content": """
        <div class="sync-container">
            <h2>数据同步状态</h2>
            <div class="sync-stats">
                <div class="stat">
                    <div class="stat-value">1,247</div>
                    <div class="stat-label">今日同步</div>
                </div>
                <div class="stat">
                    <div class="stat-value">98.7%</div>
                    <div class="stat-label">成功率</div>
                </div>
                <div class="stat">
                    <div class="stat-value">2.3s</div>
                    <div class="stat-label">平均延迟</div>
                </div>
            </div>
            <div class="recent-activity">
                <h3>最近活动</h3>
                <ul>
                    <li>用户数据同步完成 - 刚刚</li>
                    <li>配置更新已应用 - 2分钟前</li>
                    <li>备份任务执行中 - 5分钟前</li>
                </ul>
            </div>
        </div>
        """,
        "style": """
        .sync-container { max-width: 800px; margin: 50px auto; padding: 30px; background: #fff; border-radius: 15px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }
        .sync-stats { display: flex; justify-content: space-around; margin: 30px 0; }
        .stat { text-align: center; }
        .stat-value { font-size: 2.5em; font-weight: bold; color: #007bff; }
        .stat-label { color: #666; margin-top: 5px; }
        .recent-activity ul { list-style: none; padding: 0; }
        .recent-activity li { padding: 8px; background: #f8f9fa; margin: 5px 0; border-radius: 5px; }
        """
    },
    {
        "title": "系统监控面板",
        "content": """
        <div class="monitor-container">
            <h2>实时系统监控</h2>
            <div class="metrics">
                <div class="metric">
                    <div class="metric-title">CPU使用率</div>
                    <div class="metric-bar">
                        <div class="metric-fill" style="width: 45%"></div>
                    </div>
                    <div class="metric-value">45%</div>
                </div>
                <div class="metric">
                    <div class="metric-title">内存使用</div>
                    <div class="metric-bar">
                        <div class="metric-fill" style="width: 68%"></div>
                    </div>
                    <div class="metric-value">68%</div>
                </div>
                <div class="metric">
                    <div class="metric-title">网络流量</div>
                    <div class="metric-bar">
                        <div class="metric-fill" style="width: 32%"></div>
                    </div>
                    <div class="metric-value">32%</div>
                </div>
            </div>
            <div class="alerts">
                <h3>系统告警</h3>
                <div class="alert info">所有系统运行正常</div>
            </div>
        </div>
        """,
        "style": """
        .monitor-container { max-width: 700px; margin: 50px auto; padding: 25px; background: #f8f9fa; border-radius: 10px; }
        .metrics { margin: 20px 0; }
        .metric { margin: 15px 0; }
        .metric-title { font-weight: bold; margin-bottom: 5px; }
        .metric-bar { width: 100%; height: 20px; background: #e9ecef; border-radius: 10px; overflow: hidden; }
        .metric-fill { height: 100%; background: linear-gradient(90deg, #28a745, #20c997); transition: width 0.3s; }
        .metric-value { text-align: right; margin-top: 5px; }
        .alert { padding: 10px; border-radius: 5px; margin: 10px 0; }
        .alert.info { background: #d1ecf1; color: #0c5460; }
        """
    }
]

# 请求计数器
request_counter = 0

def log_message(message):
    """增强的日志函数，确保日志立即输出"""
    timestamp = datetime.datetime.now().strftime('%H:%M:%S')
    full_message = f"[{timestamp}] {message}"
    print(full_message, flush=True)  # 强制立即刷新

def generate_simulated_page():
    """生成仿真页面"""
    global request_counter
    request_counter += 1
    
    page_template = random.choice(SIMULATED_PAGES)
    current_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    # 替换模板中的变量
    content = page_template["content"].format(
        timestamp=current_time,
        requests=request_counter
    )
    
    html = f"""
    <!DOCTYPE html>
    <html lang="zh-CN">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>{page_template["title"]}</title>
        <style>
            body {{
                font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
                margin: 0;
                padding: 20px;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                min-height: 100vh;
                color: #333;
            }}
            {page_template["style"]}
            .footer {{
                text-align: center;
                margin-top: 30px;
                color: rgba(255,255,255,0.7);
                font-size: 0.9em;
            }}
        </style>
    </head>
    <body>
        {content}
        <div class="footer">
            <p>系统自动生成 • 最后更新: {current_time}</p>
        </div>
    </body>
    </html>
    """
    return html

async def health_check(request):
    """健康检查端点，返回仿真页面"""
    path = request.path
    
    # 如果是API端点，返回JSON
    if path == '/api/health':
        return web.json_response({
            "status": "healthy",
            "service": "api-gateway",
            "timestamp": datetime.datetime.now().isoformat(),
            "version": "1.0",
            "requests": request_counter
        })
    elif path == '/api/stats':
        return web.json_response({
            "uptime": int(time.time() - start_time),
            "requests": request_counter,
            "active_connections": random.randint(50, 200)
        })
    
    # 其他路径返回仿真HTML页面
    html_content = generate_simulated_page()
    return web.Response(text=html_content, content_type='text/html')

async def internal_keep_alive():
    """高频内部保活"""
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(
                f'http://localhost:{CONFIG["internal_port"]}/health',
                timeout=3
            ) as resp:
                log_message("内部保活成功")
                return True
    except Exception as e:
        log_message(f"内部保活失败: {str(e)[:30]}")
        return False

async def external_keep_alive():
    """高频外部保活"""
    try:
        # 随机选择路径，增加多样性
        paths = ['/', '/health', '/status', '/api/health', '/api/stats']
        path = random.choice(paths)
        url = f'https://{CONFIG["domain"]}{path}'
        
        async with aiohttp.ClientSession() as session:
            headers = {'User-Agent': random.choice(CONFIG['user_agents'])}
            async with session.get(url, headers=headers, timeout=8) as resp:
                status_info = f"{resp.status}"
                if path.startswith('/api'):
                    # 如果是API调用，记录响应内容摘要
                    try:
                        data = await resp.json()
                        status_info = f"{resp.status} {str(data)[:50]}..."
                    except:
                        pass
                log_message(f"外部流量: {status_info} {path}")
                return True
    except Exception as e:
        log_message(f"外部保活: {str(e)[:30]}")
        return True

async def keep_alive_task():
    """超高频保活任务"""
    cycle_count = 0
    while True:
        try:
            # 内部保活
            await internal_keep_alive()
            
            # 每3次循环执行一次外部保活
            if cycle_count % 3 == 0:
                await external_keep_alive()
            
            # 极短间隔：8-12秒
            sleep_time = random.randint(8, 12)
            log_message(f"等待 {sleep_time}秒")
            await asyncio.sleep(sleep_time)
            
            cycle_count += 1
            
        except Exception as e:
            log_message(f"保活异常: {str(e)[:30]}")
            await asyncio.sleep(10)

def create_app():
    app = web.Application()
    # 注册所有路由
    app.router.add_get('/', health_check)
    app.router.add_get('/health', health_check)
    app.router.add_get('/status', health_check)
    app.router.add_get('/api/health', health_check)
    app.router.add_get('/api/stats', health_check)
    return app

async def start_background_tasks(app):
    app['keep_alive'] = asyncio.create_task(keep_alive_task())

async def cleanup_background_tasks(app):
    if 'keep_alive' in app:
        app['keep_alive'].cancel()
        try:
            await app['keep_alive']
        except asyncio.CancelledError:
            log_message("保活任务已停止")

# 记录启动时间
start_time = time.time()

if __name__ == "__main__":
    log_message("启动超高频防休眠服务")
    log_message("保活间隔: 8-12秒")
    log_message("外部流量: 每24-36秒一次")
    log_message("仿真页面: 已启用多种页面类型")
    
    app = create_app()
    app.on_startup.append(start_background_tasks)
    app.on_cleanup.append(cleanup_background_tasks)
    
    web.run_app(app, host='0.0.0.0', port=CONFIG['internal_port'], print=None)

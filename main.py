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
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.1 Safari/605.1.15",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36",
        "Mozilla/5.0 (iPhone; CPU iPhone OS 15_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Mobile/15E148 Safari/604.1",
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
        "/", "/home", "/about", "/contact", "/privacy", "/terms", 
        "/blog", "/news", "/products", "/services", "/faq", "/help",
        "/api/v1/status", "/api/v1/info", "/health", "/status"
    ],
    "search_terms": [
        "云原生技术", "Web开发", "API设计", "网络安全", "容器化部署",
        "微服务架构", "自动化运维", "前后端分离", "RESTful API", "认证授权"
    ]
}

def generate_normal_website():
    """生成完整的网页内容 - 无删减版本"""
    websites = [
        # 个人博客样式 - 完整内容
        """<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>技术笔记 | 个人博客</title>
    <style>
        body { 
            font-family: Arial, sans-serif; 
            margin: 0; 
            padding: 20px; 
            background: #f5f5f5; 
            line-height: 1.6;
        }
        .container { 
            max-width: 800px; 
            margin: 0 auto; 
            background: white; 
            padding: 30px; 
            border-radius: 8px; 
            box-shadow: 0 2px 10px rgba(0,0,0,0.1); 
        }
        h1 { 
            color: #333; 
            border-bottom: 2px solid #eee; 
            padding-bottom: 10px; 
            margin-bottom: 30px;
        }
        .post { 
            margin-bottom: 30px; 
            padding-bottom: 20px;
            border-bottom: 1px solid #eee;
        }
        .post:last-child {
            border-bottom: none;
        }
        .date { 
            color: #666; 
            font-size: 0.9em; 
            margin-bottom: 10px;
        }
        .content { 
            line-height: 1.6; 
        }
        .content p {
            margin-bottom: 15px;
        }
        .tags {
            margin-top: 15px;
        }
        .tag {
            display: inline-block;
            background: #e9ecef;
            padding: 3px 8px;
            border-radius: 4px;
            font-size: 0.8em;
            margin-right: 5px;
            color: #495057;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>技术学习笔记</h1>
        
        <div class="post">
            <h2>关于云部署的一些思考与实践</h2>
            <div class="date">2024年10月26日</div>
            <div class="content">
                <p>最近在研究云原生技术的应用，发现容器化部署确实带来了很多便利。特别是在微服务架构下，每个服务都可以独立部署和扩展，大大提高了系统的灵活性和可维护性。</p>
                <p>自动化运维工具的使用显著提升了开发效率，让我们能够更专注于业务逻辑的实现，而不是基础设施的管理。</p>
                <p>在实际部署过程中，需要考虑的因素包括网络配置、安全策略、资源分配等多个方面，需要综合权衡。</p>
                <div class="tags">
                    <span class="tag">云原生</span>
                    <span class="tag">容器化</span>
                    <span class="tag">微服务</span>
                </div>
            </div>
        </div>
        
        <div class="post">
            <h2>Web开发最佳实践与架构设计</h2>
            <div class="date">2024年10月25日</div>
            <div class="content">
                <p>现代Web开发中，前后端分离已经成为主流趋势。RESTful API的设计要遵循一定的规范，保证接口的易用性和可维护性。</p>
                <p>安全性也是不可忽视的一环，合理的认证授权机制是保障系统安全的基础。同时需要考虑性能优化、缓存策略、数据库设计等多个方面。</p>
                <p>在架构设计时，要考虑到系统的可扩展性、可维护性和性能要求，选择合适的架构模式和技術栈。</p>
                <div class="tags">
                    <span class="tag">Web开发</span>
                    <span class="tag">RESTful API</span>
                    <span class="tag">架构设计</span>
                </div>
            </div>
        </div>
        
        <div class="post">
            <h2>系统监控与性能优化策略</h2>
            <div class="date">2024年10月24日</div>
            <div class="content">
                <p>系统监控是保障服务稳定运行的重要手段。通过实时监控系统指标，可以及时发现和解决潜在问题。</p>
                <p>性能优化需要从多个层面入手，包括代码优化、数据库优化、网络优化等。要使用合适的工具和方法进行性能分析和调优。</p>
                <p>建立完善的日志系统和告警机制，可以帮助我们快速定位和解决问题，提高系统的可靠性。</p>
                <div class="tags">
                    <span class="tag">系统监控</span>
                    <span class="tag">性能优化</span>
                    <span class="tag">日志系统</span>
                </div>
            </div>
        </div>
    </div>
</body>
</html>""",

        # 服务状态页面 - 完整内容
        """<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>系统状态监控</title>
    <style>
        body { 
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; 
            margin: 0; 
            padding: 20px; 
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
            color: white;
            min-height: 100vh;
        }
        .container { 
            max-width: 600px; 
            margin: 50px auto; 
            background: rgba(255,255,255,0.1); 
            padding: 30px; 
            border-radius: 15px; 
            backdrop-filter: blur(10px);
            box-shadow: 0 8px 32px rgba(0,0,0,0.1);
        }
        h1 { 
            text-align: center; 
            margin-bottom: 30px;
            font-weight: 300;
            letter-spacing: 1px;
        }
        .status-card { 
            background: rgba(255,255,255,0.2); 
            padding: 20px; 
            border-radius: 10px; 
            margin-bottom: 20px;
            border: 1px solid rgba(255,255,255,0.3);
        }
        .status-item { 
            display: flex; 
            justify-content: space-between; 
            margin-bottom: 10px;
            padding: 8px 0;
            border-bottom: 1px solid rgba(255,255,255,0.1);
        }
        .status-item:last-child {
            border-bottom: none;
            margin-bottom: 0;
        }
        .label { 
            flex: 1; 
            font-weight: bold;
            opacity: 0.9;
        }
        .value { 
            flex: 2;
            text-align: right;
        }
        .online { 
            color: #4CAF50;
            font-weight: bold;
        }
        .warning { 
            color: #FFC107;
        }
        .metric-grid {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 15px;
            margin-top: 20px;
        }
        .metric-card {
            background: rgba(255,255,255,0.15);
            padding: 15px;
            border-radius: 8px;
            text-align: center;
        }
        .metric-value {
            font-size: 1.5em;
            font-weight: bold;
            margin: 10px 0;
        }
        .metric-label {
            font-size: 0.8em;
            opacity: 0.8;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>系统状态监控面板</h1>
        <div class="status-card">
            <div class="status-item">
                <span class="label">服务状态:</span>
                <span class="value online">正常运行</span>
            </div>
            <div class="status-item">
                <span class="label">最后检查:</span>
                <span class="value">""" + datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + """</span>
            </div>
            <div class="status-item">
                <span class="label">运行时间:</span>
                <span class="value">""" + str(random.randint(100, 1000)) + """ 天</span>
            </div>
            <div class="status-item">
                <span class="label">内存使用:</span>
                <span class="value">""" + str(random.randint(30, 80)) + """%</span>
            </div>
            <div class="status-item">
                <span class="label">CPU负载:</span>
                <span class="value">""" + str(round(random.uniform(0.1, 2.0), 1)) + """%</span>
            </div>
        </div>
        
        <div class="metric-grid">
            <div class="metric-card">
                <div class="metric-label">请求数量</div>
                <div class="metric-value">""" + str(random.randint(1000, 10000)) + """</div>
            </div>
            <div class="metric-card">
                <div class="metric-label">响应时间</div>
                <div class="metric-value">""" + str(random.randint(10, 100)) + """ms</div>
            </div>
            <div class="metric-card">
                <div class="metric-label">在线用户</div>
                <div class="metric-value">""" + str(random.randint(1, 50)) + """</div>
            </div>
            <div class="metric-card">
                <div class="metric-label">错误率</div>
                <div class="metric-value">""" + str(round(random.uniform(0.01, 0.5), 2)) + """%</div>
            </div>
        </div>
        
        <p style="text-align: center; opacity: 0.8; font-size: 0.9em; margin-top: 30px;">
            系统监控页面 - 自动更新 | 最后刷新: """ + datetime.datetime.now().strftime("%H:%M:%S") + """
        </p>
    </div>
</body>
</html>""",

        # API文档页面 - 完整内容
        """<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>API 文档中心</title>
    <style>
        body { 
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; 
            margin: 0; 
            padding: 20px; 
            background: #1a1a1a; 
            color: #e0e0e0;
            line-height: 1.6;
        }
        .container { 
            max-width: 800px; 
            margin: 0 auto;
        }
        header { 
            text-align: center; 
            margin-bottom: 40px;
            padding-bottom: 20px;
            border-bottom: 1px solid #333;
        }
        h1 { 
            color: #fff; 
            margin-bottom: 10px;
            font-weight: 300;
        }
        .description {
            opacity: 0.8;
            max-width: 600px;
            margin: 0 auto;
        }
        .api-section { 
            background: #2d2d2d; 
            padding: 25px; 
            border-radius: 8px; 
            margin-bottom: 20px;
            border-left: 4px solid #4CAF50;
        }
        .method { 
            display: inline-block; 
            background: #4CAF50; 
            color: white; 
            padding: 5px 10px; 
            border-radius: 4px; 
            font-weight: bold; 
            margin-right: 10px;
            font-family: monospace;
            font-size: 0.9em;
        }
        .endpoint { 
            font-family: monospace; 
            color: #bb86fc;
            font-size: 1.1em;
        }
        .api-description {
            margin: 15px 0;
            opacity: 0.9;
        }
        .parameter-table {
            width: 100%;
            border-collapse: collapse;
            margin: 15px 0;
            background: #3d3d3d;
            border-radius: 4px;
            overflow: hidden;
        }
        .parameter-table th {
            background: #4d4d4d;
            padding: 10px;
            text-align: left;
            font-weight: 600;
        }
        .parameter-table td {
            padding: 10px;
            border-bottom: 1px solid #4d4d4d;
        }
        .parameter-table tr:last-child td {
            border-bottom: none;
        }
        .code-block {
            background: #2d2d2d;
            padding: 15px;
            border-radius: 4px;
            border-left: 4px solid #bb86fc;
            margin: 15px 0;
            overflow-x: auto;
        }
        .code-block code {
            font-family: 'Courier New', monospace;
            color: #e0e0e0;
        }
        .response-example {
            background: #2d2d2d;
            padding: 15px;
            border-radius: 4px;
            margin: 15px 0;
        }
    </style>
</head>
<body>
    <div class="container">
        <header>
            <h1>API 文档中心</h1>
            <p class="description">欢迎使用我们的服务接口文档，这里提供了完整的API接口说明和使用示例。</p>
        </header>
        
        <div class="api-section">
            <div><span class="method">GET</span> <span class="endpoint">/api/v1/status</span></div>
            <div class="api-description">
                <p>获取服务状态信息，包括运行状态、资源使用情况等。</p>
            </div>
            <table class="parameter-table">
                <thead>
                    <tr>
                        <th>参数</th>
                        <th>类型</th>
                        <th>说明</th>
                    </tr>
                </thead>
                <tbody>
                    <tr>
                        <td>format</td>
                        <td>string</td>
                        <td>返回格式，可选值: json, xml (默认: json)</td>
                    </tr>
                </tbody>
            </table>
            <div class="response-example">
                <strong>响应示例:</strong>
                <div class="code-block">
                    <code>{
  "status": "healthy",
  "timestamp": "2024-10-26T07:46:14Z",
  "version": "1.0.0",
  "uptime": 123456,
  "memory_usage": 45.2
}</code>
                </div>
            </div>
        </div>
        
        <div class="api-section">
            <div><span class="method">POST</span> <span class="endpoint">/api/v1/data</span></div>
            <div class="api-description">
                <p>提交数据处理请求，支持多种数据格式和处理选项。</p>
            </div>
            <table class="parameter-table">
                <thead>
                    <tr>
                        <th>参数</th>
                        <th>类型</th>
                        <th>说明</th>
                    </tr>
                </thead>
                <tbody>
                    <tr>
                        <td>data</td>
                        <td>object</td>
                        <td>要处理的数据对象</td>
                    </tr>
                    <tr>
                        <td>options</td>
                        <td>object</td>
                        <td>处理选项配置</td>
                    </tr>
                </tbody>
            </table>
        </div>
        
        <div class="api-section">
            <div><span class="method">GET</span> <span class="endpoint">/api/v1/info</span></div>
            <div class="api-description">
                <p>获取系统信息，包括版本信息、配置参数等。</p>
            </div>
            <div class="response-example">
                <strong>响应示例:</strong>
                <div class="code-block">
                    <code>{
  "service": "api-gateway",
  "version": "1.0.0",
  "environment": "production",
  "features": ["auth", "cache", "monitoring"]
}</code>
                </div>
            </div>
        </div>
    </div>
</body>
</html>"""
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
            "requests_served": random.randint(1000, 10000),
            "memory_usage": round(random.uniform(30.0, 80.0), 1),
            "cpu_load": round(random.uniform(0.1, 2.0), 1)
        })
    else:
        return web.Response(text=generate_normal_website(), content_type='text/html')

async def internal_keep_alive():
    """内部保活：高频访问本地健康检查"""
    try:
        async with aiohttp.ClientSession() as session:
            headers = {'User-Agent': random.choice(CONFIG['user_agents'])}
            async with session.get(
                f'http://localhost:{CONFIG["internal_port"]}/health',
                headers=headers,
                timeout=3
            ) as resp:
                print(f"[{datetime.datetime.now().strftime('%H:%M:%S')}] 内部保活成功: {resp.status}")
                return True
    except Exception as e:
        print(f"[{datetime.datetime.now().strftime('%H:%M:%S')}] 内部保活失败: {str(e)[:30]}")
        return False

async def external_keep_alive():
    """外部保活：高频模拟真实用户流量"""
    try:
        path = random.choice(CONFIG['paths'])
        
        # 随机生成查询参数
        query_params = {}
        if random.random() > 0.2:  # 80%概率添加查询参数
            query_params['q'] = random.choice(CONFIG['search_terms'])
            query_params['page'] = str(random.randint(1, 10))
            query_params['sort'] = random.choice(['asc', 'desc'])
            if random.random() > 0.5:
                query_params['filter'] = random.choice(['latest', 'popular', 'featured'])
        
        query_string = urllib.parse.urlencode(query_params)
        url = f'https://{CONFIG["domain"]}{path}'
        if query_string:
            url += f'?{query_string}'
        
        async with aiohttp.ClientSession() as session:
            headers = {
                'User-Agent': random.choice(CONFIG['user_agents']),
                'Referer': random.choice(CONFIG['referrers']),
                'Accept-Language': random.choice(['en-US,en;q=0.9', 'zh-CN,zh;q=0.8']),
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8'
            }
            
            # 随机选择请求方法
            if random.random() > 0.7:  # 30%概率使用POST
                data = {'key': ''.join(random.choices('abcdefghijklmnopqrstuvwxyz', k=8))}
                async with session.post(url, headers=headers, data=data, timeout=8) as resp:
                    print(f"[{datetime.datetime.now().strftime('%H:%M:%S')}] 外部POST流量: {resp.status} {path}")
            else:  # 70%概率使用GET
                async with session.get(url, headers=headers, timeout=8) as resp:
                    print(f"[{datetime.datetime.now().strftime('%H:%M:%S')}] 外部GET流量: {resp.status} {path}")
                    
        return True
    except Exception as e:
        print(f"[{datetime.datetime.now().strftime('%H:%M:%S')}] 外部保活错误: {str(e)[:30]}")
        return True

async def keep_alive_task():
    """高频保活任务 - 5-8秒间隔确保不被停止"""
    cycle_count = 0
    while True:
        try:
            # 并行执行内部和外部保活
            internal_task = asyncio.create_task(internal_keep_alive())
            external_task = asyncio.create_task(external_keep_alive())
            
            await asyncio.gather(internal_task, external_task, return_exceptions=True)
            
            # 高频间隔：5-8秒（确保300秒内有足够活动）
            sleep_time = random.randint(5, 8)
            await asyncio.sleep(sleep_time)
            
            cycle_count += 1
            
        except Exception as e:
            print(f"[{datetime.datetime.now().strftime('%H:%M:%S')}] 保活任务异常: {str(e)[:30]}")
            await asyncio.sleep(10)

def create_app():
    app = web.Application()
    app.router.add_get('/', health_check)
    app.router.add_get('/health', health_check)
    app.router.add_get('/status', health_check)
    app.router.add_get('/api/v1/info', health_check)
    app.router.add_get('/api/v1/status', health_check)
    app.router.add_get('/about', health_check)
    app.router.add_get('/contact', health_check)
    app.router.add_get('/blog', health_check)
    app.router.add_get('/news', health_check)
    return app

async def start_background_tasks(app):
    app['keep_alive'] = asyncio.create_task(keep_alive_task())

async def cleanup_background_tasks(app):
    if 'keep_alive' in app:
        app['keep_alive'].cancel()
        try:
            await app['keep_alive']
        except asyncio.CancelledError:
            print("保活任务已安全停止")

if __name__ == "__main__":
    print("启动高频防休眠服务...")
    print(f"保活间隔: 5-8秒")
    print(f"服务端口: {CONFIG['internal_port']}")
    print(f"公网地址: https://{CONFIG['domain']}")
    
    app = create_app()
    app.on_startup.append(start_background_tasks)
    app.on_cleanup.append(cleanup_background_tasks)
    
    web.run_app(
        app, 
        host='0.0.0.0', 
        port=CONFIG['internal_port'], 
        print=None
    )

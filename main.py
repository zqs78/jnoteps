#!/usr/bin/env python3
from aiohttp import web
import sys
import aiohttp
import asyncio
import random
import time
import datetime
import urllib.parse

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
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.1 Safari/605.1.15",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36",
        "Mozilla/5.0 (iPhone; CPU iPhone OS 15_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Mobile/15E148 Safari/604.1",
        "Mozilla/5.0 (Android 12; Mobile; rv:90.0) Gecko/90.0 Firefox/90.0"
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
        "/blog", "/news", "/products", "/services", "/faq", "/help"
    ],
    "search_terms": [
        "云原生技术", "Web开发", "API设计", "网络安全", "容器化部署",
        "微服务架构", "自动化运维", "前后端分离", "RESTful API", "认证授权"
    ]
}

def generate_normal_website():
    """生成一个看起来正常的网页内容"""
    websites = [
        # 精简版个人博客
        """<!DOCTYPE html><html><head><meta charset="UTF-8"><title>技术笔记</title><style>body{font-family:Arial;margin:20px}</style></head><body><h1>技术学习笔记</h1><p>最近在研究云原生技术应用。</p></body></html>""",
        
        # 精简版状态页面
        """<!DOCTYPE html><html><head><meta charset="UTF-8"><title>系统监控</title><style>body{font-family:Segoe UI;background:#667eea;color:white}</style></head><body><h1>系统状态监控</h1><p>服务运行正常</p></body></html>"""
    ]
    return random.choice(websites)

async def health_check(request):
    """健康检查端点"""
    if request.path == '/health' or request.path == '/status':
        return web.json_response({
            "status": "healthy",
            "service": "api-gateway",
            "timestamp": datetime.datetime.now().isoformat(),
            "version": "1.0"
        })
    else:
        return web.Response(text=generate_normal_website(), content_type='text/html')

async def internal_keep_alive():
    """内部保活：访问本地健康检查接口"""
    try:
        async with aiohttp.ClientSession() as session:
            headers = {'User-Agent': random.choice(CONFIG['user_agents'])}
            async with session.get(
                f'http://localhost:{CONFIG["internal_port"]}/health',
                headers=headers,
                timeout=5
            ) as resp:
                print(f"[{datetime.datetime.now().strftime('%H:%M:%S')}] 内部保活成功 - 状态: {resp.status}")
                return True
    except Exception as e:
        print(f"[{datetime.datetime.now().strftime('%H:%M:%S')}] 内部保活失败: {str(e)[:50]}")
        return False

async def simulate_real_traffic():
    """模拟真实用户流量"""
    try:
        path = random.choice(CONFIG['paths'])
        
        # 随机生成查询参数
        query_params = {}
        if random.random() > 0.3:  # 70%的概率添加查询参数
            query_params['q'] = random.choice(CONFIG['search_terms'])
            query_params['page'] = str(random.randint(1, 10))
            query_params['sort'] = random.choice(['asc', 'desc'])
        
        query_string = urllib.parse.urlencode(query_params)
        url = f'https://{CONFIG["domain"]}{path}'
        if query_string:
            url += f'?{query_string}'
        
        async with aiohttp.ClientSession() as session:
            headers = {
                'User-Agent': random.choice(CONFIG['user_agents']),
                'Referer': random.choice(CONFIG['referrers']),
                'Accept-Language': random.choice(['en-US,en;q=0.9', 'zh-CN,zh;q=0.8'])
            }
            
            # 随机选择请求方法
            if random.random() > 0.8:  # 20%概率使用POST
                data = {'key': ''.join(random.choices('abcdefghijklmnopqrstuvwxyz', k=8))}
                async with session.post(url, headers=headers, data=data, timeout=8) as resp:
                    print(f"[{datetime.datetime.now().strftime('%H:%M:%S')}] 模拟POST流量: {resp.status} {path}")
            else:  # 80%概率使用GET
                async with session.get(url, headers=headers, timeout=8) as resp:
                    print(f"[{datetime.datetime.now().strftime('%H:%M:%S')}] 模拟GET流量: {resp.status} {path}")
                    
        return True
    except Exception as e:
        print(f"[{datetime.datetime.now().strftime('%H:%M:%S')}] 流量模拟错误: {str(e)[:50]}")
        return True

async def keep_alive_cycle():
    """增强型保活循环"""
    cycle_count = 0
    while True:
        try:
            # 内部健康检查
            await internal_keep_alive()
            
            # 每3次循环模拟一次真实流量
            if cycle_count % 3 == 0:
                await simulate_real_traffic()
            
            # 动态间隔 (10-15秒)
            sleep_time = random.randint(10, 15)
            await asyncio.sleep(sleep_time)
            
            cycle_count += 1
            
        except Exception as e:
            print(f"[{datetime.datetime.now().strftime('%H:%M:%S')}] 保活异常: {str(e)[:50]}")
            await asyncio.sleep(15)

app = web.Application()
app.router.add_get('/', health_check)
app.router.add_get('/health', health_check)
app.router.add_get('/status', health_check)

async def start_background_tasks(app):
    """启动后台任务"""
    app['keep_alive'] = asyncio.create_task(keep_alive_cycle())

async def cleanup_background_tasks(app):
    """清理后台任务"""
    if 'keep_alive' in app:
        app['keep_alive'].cancel()
        try:
            await app['keep_alive']
        except asyncio.CancelledError:
            print("保活任务已安全停止")

if __name__ == "__main__":
    print("启动增强型防休眠服务...")
    
    # 创建应用
    app = web.Application()
    app.on_startup.append(start_background_tasks)
    app.on_cleanup.append(cleanup_background_tasks)
    
    # 启动Web服务
    web.run_app(
        app, 
        host='0.0.0.0', 
        port=CONFIG['internal_port'], 
        print=lambda *args: None  # 禁用默认日志
    )

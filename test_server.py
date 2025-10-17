#!/usr/bin/env python3
import sys
import subprocess
import signal
import time

def test_server(server_path):
    """测试MCP服务器是否能正常启动"""
    try:
        print(f"正在测试服务器: {server_path}")
        
        # 启动服务器进程
        process = subprocess.Popen(
            [sys.executable, server_path],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        
        # 等待2秒看是否有错误
        time.sleep(2)
        
        # 检查进程状态
        poll_result = process.poll()
        
        if poll_result is None:
            # 进程仍在运行，说明启动成功
            print("✅ 服务器启动成功")
            process.terminate()
            process.wait(timeout=5)
            return True
        else:
            # 进程已退出，可能有错误
            stdout, stderr = process.communicate()
            print(f"❌ 服务器启动失败")
            if stderr:
                print(f"错误输出: {stderr}")
            if stdout:
                print(f"标准输出: {stdout}")
            return False
            
    except Exception as e:
        print(f"❌ 测试过程中出错: {e}")
        return False

if __name__ == "__main__":
    servers = [
        "mcp_servers/getDomainInfo_server.py",
        "mcp_servers/weather_server.py",
        "mcp_servers/getSysInfo_server.py",
        "mcp_servers/ip_location_server.py"
    ]
    
    results = {}
    for server in servers:
        results[server] = test_server(server)
        print("-" * 50)
    
    print("\n📊 测试结果汇总:")
    for server, success in results.items():
        status = "✅ 成功" if success else "❌ 失败"
        print(f"  {server}: {status}")
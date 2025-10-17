#!/usr/bin/env python3
"""
域名信息查询服务快速测试脚本
简化版测试，专门测试 www.baidu.com 域名查询
"""

import asyncio
import sys
import os
from datetime import datetime

# 添加当前目录到 Python 路径
sys.path.append(os.path.dirname(__file__))

try:
    from mcp_servers.getDomainInfo_server import query_domain, batch_query_domains, check_domain_availability
    print("✅ 成功导入域名查询服务模块")
except ImportError as e:
    print(f"❌ 导入模块失败: {e}")
    print("请确保已安装所需依赖: pip install -r requirements.txt")
    sys.exit(1)


async def test_baidu_domain():
    """测试百度域名查询"""
    domain = "www.baidu.com"
    
    print("🌐 域名信息查询服务测试")
    print("=" * 50)
    print(f"测试域名: {domain}")
    print(f"测试时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    # 测试 1: 单个域名查询
    print("📋 测试 1: 单个域名查询")
    print("-" * 30)
    try:
        result1 = await query_domain(domain)
        print(result1)
        print("✅ 单个域名查询测试通过")
    except Exception as e:
        print(f"❌ 单个域名查询测试失败: {e}")
    
    print("\n" + "=" * 50 + "\n")
    
    # 测试 2: 批量域名查询
    print("📋 测试 2: 批量域名查询")
    print("-" * 30)
    try:
        batch_domains = "www.baidu.com,www.google.com"
        result2 = await batch_query_domains(batch_domains)
        print(result2)
        print("✅ 批量域名查询测试通过")
    except Exception as e:
        print(f"❌ 批量域名查询测试失败: {e}")
    
    print("\n" + "=" * 50 + "\n")
    
    # 测试 3: 域名可用性检查
    print("📋 测试 3: 域名可用性检查")
    print("-" * 30)
    try:
        result3 = await check_domain_availability(domain)
        print(result3)
        print("✅ 域名可用性检查测试通过")
    except Exception as e:
        print(f"❌ 域名可用性检查测试失败: {e}")
    
    print("\n" + "=" * 50)
    print("🎉 所有测试完成！")


if __name__ == "__main__":
    print("启动域名查询服务测试...")
    print()
    
    # 运行异步测试
    try:
        asyncio.run(test_baidu_domain())
    except KeyboardInterrupt:
        print("\n⚠️ 测试被用户中断")
    except Exception as e:
        print(f"\n❌ 测试执行出错: {e}")
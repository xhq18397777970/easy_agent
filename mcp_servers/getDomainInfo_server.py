import os
import json
import whois
from datetime import datetime
from typing import Any
from dotenv import load_dotenv
from mcp.server.fastmcp import FastMCP

# 初始化 MCP 服务器
mcp = FastMCP("DomainInfoServer")

# 加载环境变量
load_dotenv()

"""
查询域名注册状态和基本信息
:param domain: 域名
:return: 域名信息字典或含 error 的字典
"""
def fetch_domain_info(domain: str) -> dict[str, Any]:
    """
    从 WHOIS 查询域名信息
    :param domain: 域名（如 google.com）
    :return: 域名数据字典；若出错返回包含 error 信息的字典
    """
    try:
        # 查询域名信息
        domain_info = whois.whois(domain)
        
        # 判断域名是否被注册
        is_registered = domain_info.status is not None and len(domain_info.status) > 0
        
        result = {
            'domain': domain,
            'is_registered': is_registered,
            'status': domain_info.status,
            'registrar': domain_info.registrar,
            'creation_date': domain_info.creation_date,
            'expiration_date': domain_info.expiration_date,
            'name_servers': domain_info.name_servers,
            'query_time': datetime.now().isoformat()
        }
        
        return result
        
    except Exception as e:
        return {
            'domain': domain,
            'error': str(e),
            'query_time': datetime.now().isoformat()
        }

def format_domain_info(data: dict[str, Any]) -> str:
    """
    将域名数据格式化为易读文本
    :param data: 域名数据字典
    :return: 格式化后的域名信息字符串
    """
    # 如果数据中包含错误信息，直接返回错误提示
    if "error" in data:
        return f"❌ 域名查询失败: {data['error']}"

    domain = data.get("domain", "未知域名")
    is_registered = data.get("is_registered", False)
    status = data.get("status", [])
    registrar = data.get("registrar", "未知")
    creation_date = data.get("creation_date", "未知")
    expiration_date = data.get("expiration_date", "未知")
    name_servers = data.get("name_servers", [])
    query_time = data.get("query_time", "未知")

    # 格式化状态信息
    status_text = ""
    if status:
        if isinstance(status, list):
            status_text = "\n".join([f"  • {s}" for s in status])
        else:
            status_text = f"  • {status}"
    
    # 格式化名称服务器
    ns_text = ""
    if name_servers:
        if isinstance(name_servers, list):
            ns_text = "\n".join([f"  • {ns}" for ns in name_servers])
        else:
            ns_text = f"  • {name_servers}"

    # 格式化日期信息
    def format_date(date_val):
        if not date_val:
            return "未知"
        if isinstance(date_val, list):
            return str(date_val[0]) if date_val else "未知"
        return str(date_val)

    creation_date_fmt = format_date(creation_date)
    expiration_date_fmt = format_date(expiration_date)

    # 构建结果字符串
    result = f"""
🌐 域名查询结果: {domain}

📊 基本信息:
  ✅ 注册状态: {'已注册' if is_registered else '未注册'}
  🏢 注册商: {registrar}
  📅 创建时间: {creation_date_fmt}
  ⏰ 过期时间: {expiration_date_fmt}

🔒 域名状态:
{status_text if status_text else "  • 无状态信息"}

🌍 域名服务器:
{ns_text if ns_text else "  • 无服务器信息"}

⏱️ 查询时间: {query_time}
"""

    return result.strip()

"""
查询域名WHOIS信息
:param domain: 域名
:return: 格式化的域名信息
"""
@mcp.tool()
async def query_domain(domain: str) -> str:
    """
    输入域名，返回WHOIS查询结果，包括注册状态、注册商、创建时间、过期时间等信息。

    使用说明:
    - 支持常见顶级域名：.com, .net, .org, .cn 等
    - 返回完整的域名注册信息
    - 如果域名未注册，会显示未注册状态

    示例:
    - "google.com" -> 返回Google域名的注册信息
    - "github.com" -> 返回GitHub域名的注册信息
    - "example-test-123456.com" -> 返回未注册域名的信息

    :param domain: 域名（如 google.com）
    :return: 格式化后的域名信息
    """
    data = fetch_domain_info(domain)
    return format_domain_info(data)

"""
批量查询多个域名信息
:param domains: 域名列表（逗号分隔或列表）
:return: 格式化的批量域名信息
"""
@mcp.tool()
async def batch_query_domains(domains: str) -> str:
    """
    批量查询多个域名的WHOIS信息。

    使用说明:
    - 支持以逗号分隔的域名列表
    - 每个域名都会单独查询并返回结果
    - 适合需要比较多个域名状态的场景

    示例:
    - "google.com,github.com,baidu.com"
    - "example.com,example.net,example.org"

    :param domains: 域名列表，用逗号分隔（如 "google.com,github.com"）
    :return: 批量查询结果汇总
    """
    # 处理输入，支持逗号分隔的字符串
    if isinstance(domains, str):
        domain_list = [d.strip() for d in domains.split(',') if d.strip()]
    else:
        domain_list = domains

    if not domain_list:
        return "❌ 请输入有效的域名列表"

    results = []
    for domain in domain_list:
        data = fetch_domain_info(domain)
        formatted = format_domain_info(data)
        results.append(formatted)
    
    # 汇总结果
    summary = f"📊 批量域名查询结果汇总（共 {len(domain_list)} 个域名）\n"
    summary += "=" * 60 + "\n\n"
    summary += "\n" + "=" * 60 + "\n".join(results)
    
    return summary

"""
检查域名是否可用（未注册）
:param domain: 域名
:return: 域名可用性检查结果
"""
@mcp.tool()
async def check_domain_availability(domain: str) -> str:
    """
    快速检查域名是否可用（未注册）。

    使用说明:
    - 专注于域名可用性检查
    - 返回简明的可用性结果
    - 适合域名注册前的快速检查

    示例:
    - "desired-domain.com" -> 返回该域名是否可用

    :param domain: 要检查的域名
    :return: 域名可用性检查结果
    """
    data = fetch_domain_info(domain)
    
    if "error" in data:
        return f"❌ 检查域名 {domain} 时出错: {data['error']}"
    
    is_registered = data.get("is_registered", False)
    domain_name = data.get("domain", domain)
    
    if is_registered:
        registrar = data.get("registrar", "未知注册商")
        expiration_date = data.get("expiration_date", "未知")
        
        # 格式化过期日期
        if isinstance(expiration_date, list) and expiration_date:
            exp_date = expiration_date[0]
        else:
            exp_date = expiration_date
        
        return f"""
🔴 域名不可用: {domain_name}

该域名已被注册:
  • 注册商: {registrar}
  • 过期时间: {exp_date}

💡 建议: 尝试其他域名变体或选择不同的顶级域名
"""
    else:
        return f"""
🟢 域名可用: {domain_name}

恭喜！该域名目前未被注册，可以尝试注册。

💡 下一步: 尽快在域名注册商处注册该域名
"""

if __name__ == "__main__":
    # 以标准 I/O 方式运行 MCP 服务器
    mcp.run(transport="stdio")
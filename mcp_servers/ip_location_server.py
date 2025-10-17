import json
import re
from typing import Any, Dict, Optional
import httpx
from mcp.server.fastmcp import FastMCP

# 初始化 MCP 服务器
mcp = FastMCP("IPLocationServer")

def validate_ip_address(ip: str) -> bool:
    """
    验证IP地址格式是否正确
    :param ip: IP地址字符串
    :return: 是否为有效的IP地址
    """
    # IPv4 正则表达式
    ipv4_pattern = r'^(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$'
    
    # IPv6 正则表达式 (简化版)
    ipv6_pattern = r'^(?:[0-9a-fA-F]{1,4}:){7}[0-9a-fA-F]{1,4}$|^::1$|^::$'
    
    return bool(re.match(ipv4_pattern, ip) or re.match(ipv6_pattern, ip))

async def query_ip_location_ipapi(ip: str) -> Dict[str, Any]:
    """
    使用 ip-api.com 查询IP归属地
    :param ip: IP地址
    :return: 包含位置信息的字典
    """
    try:
        url = f"http://ip-api.com/json/{ip}?lang=zh-CN"
        
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.get(url)
            response.raise_for_status()
            data = response.json()
            
            if data.get("status") == "success":
                return {
                    "success": True,
                    "ip": ip,
                    "country": data.get("country", "未知"),
                    "country_code": data.get("countryCode", ""),
                    "region": data.get("regionName", "未知"),
                    "region_code": data.get("region", ""),
                    "city": data.get("city", "未知"),
                    "zip_code": data.get("zip", ""),
                    "latitude": data.get("lat", 0),
                    "longitude": data.get("lon", 0),
                    "timezone": data.get("timezone", ""),
                    "isp": data.get("isp", "未知"),
                    "organization": data.get("org", "未知"),
                    "as_number": data.get("as", ""),
                    "query_ip": data.get("query", ip)
                }
            else:
                return {
                    "success": False,
                    "ip": ip,
                    "error": data.get("message", "查询失败"),
                    "error_code": "API_ERROR"
                }
                
    except httpx.TimeoutException:
        return {
            "success": False,
            "ip": ip,
            "error": "请求超时，请稍后重试",
            "error_code": "TIMEOUT"
        }
    except httpx.HTTPStatusError as e:
        return {
            "success": False,
            "ip": ip,
            "error": f"HTTP错误: {e.response.status_code}",
            "error_code": "HTTP_ERROR"
        }
    except Exception as e:
        return {
            "success": False,
            "ip": ip,
            "error": f"查询过程中发生错误: {str(e)}",
            "error_code": "UNKNOWN_ERROR"
        }

async def query_ip_location_ipinfo(ip: str) -> Dict[str, Any]:
    """
    使用 ipinfo.io 作为备用API查询IP归属地
    :param ip: IP地址
    :return: 包含位置信息的字典
    """
    try:
        url = f"https://ipinfo.io/{ip}/json"
        
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.get(url)
            response.raise_for_status()
            data = response.json()
            
            # 解析位置信息
            location = data.get("loc", "").split(",")
            latitude = float(location[0]) if len(location) > 0 and location[0] else 0
            longitude = float(location[1]) if len(location) > 1 and location[1] else 0
            
            return {
                "success": True,
                "ip": ip,
                "country": data.get("country", "未知"),
                "region": data.get("region", "未知"),
                "city": data.get("city", "未知"),
                "postal": data.get("postal", ""),
                "latitude": latitude,
                "longitude": longitude,
                "timezone": data.get("timezone", ""),
                "isp": data.get("org", "未知"),
                "query_ip": data.get("ip", ip)
            }
            
    except Exception as e:
        return {
            "success": False,
            "ip": ip,
            "error": f"备用API查询失败: {str(e)}",
            "error_code": "BACKUP_API_ERROR"
        }

def format_location_info(data: Dict[str, Any]) -> str:
    """
    格式化IP位置信息为易读文本
    :param data: IP位置信息字典
    :return: 格式化后的位置信息字符串
    """
    if not data.get("success"):
        return f"❌ IP查询失败\n" \
               f"IP地址: {data.get('ip', '未知')}\n" \
               f"错误信息: {data.get('error', '未知错误')}"
    
    output = f"🌍 IP归属地查询结果\n\n"
    output += f"🔍 查询IP: {data.get('query_ip', data.get('ip', '未知'))}\n\n"
    
    # 地理位置信息
    output += f"📍 地理位置:\n"
    output += f"  国家: {data.get('country', '未知')}"
    if data.get('country_code'):
        output += f" ({data.get('country_code')})"
    output += f"\n"
    
    if data.get('region'):
        output += f"  省份/州: {data.get('region')}"
        if data.get('region_code'):
            output += f" ({data.get('region_code')})"
        output += f"\n"
    
    output += f"  城市: {data.get('city', '未知')}\n"
    
    if data.get('zip_code') or data.get('postal'):
        zip_code = data.get('zip_code') or data.get('postal')
        output += f"  邮编: {zip_code}\n"
    
    # 坐标信息
    lat = data.get('latitude', 0)
    lon = data.get('longitude', 0)
    if lat != 0 or lon != 0:
        output += f"\n🗺️ 坐标信息:\n"
        output += f"  纬度: {lat}\n"
        output += f"  经度: {lon}\n"
    
    # 网络信息
    output += f"\n🌐 网络信息:\n"
    output += f"  ISP: {data.get('isp', '未知')}\n"
    
    if data.get('organization'):
        output += f"  组织: {data.get('organization')}\n"
    
    if data.get('as_number'):
        output += f"  AS号: {data.get('as_number')}\n"
    
    # 时区信息
    if data.get('timezone'):
        output += f"\n⏰ 时区: {data.get('timezone')}\n"
    
    return output

@mcp.tool()
async def query_ip_location(ip_address: str) -> str:
    """
    查询IP地址的归属地信息
    
    功能说明:
    - 支持IPv4和IPv6地址查询
    - 返回国家、省份、城市等地理位置信息
    - 提供ISP、组织、时区等网络信息
    - 包含经纬度坐标信息
    - 自动验证IP地址格式
    - 使用多个API确保查询成功率
    
    参数:
    - ip_address: 要查询的IP地址 (例如: "8.8.8.8" 或 "2001:4860:4860::8888")
    
    返回:
    格式化的IP归属地信息报告
    """
    # 验证IP地址格式
    if not validate_ip_address(ip_address):
        return f"❌ 无效的IP地址格式: {ip_address}\n" \
               f"请输入有效的IPv4或IPv6地址\n" \
               f"例如: 8.8.8.8 或 2001:4860:4860::8888"
    
    # 首先尝试主要API
    result = await query_ip_location_ipapi(ip_address)
    
    # 如果主要API失败，尝试备用API
    if not result.get("success"):
        backup_result = await query_ip_location_ipinfo(ip_address)
        if backup_result.get("success"):
            result = backup_result
    
    return format_location_info(result)

@mcp.tool()
async def get_my_ip_location() -> str:
    """
    查询当前公网IP地址及其归属地信息
    
    功能说明:
    - 自动获取当前的公网IP地址
    - 查询该IP的详细归属地信息
    - 无需手动输入IP地址
    
    返回:
    当前IP的归属地信息报告
    """
    try:
        # 获取当前公网IP
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.get("https://api.ipify.org?format=json")
            response.raise_for_status()
            ip_data = response.json()
            current_ip = ip_data.get("ip")
            
            if not current_ip:
                return "❌ 无法获取当前公网IP地址"
            
            # 查询IP归属地
            result = await query_ip_location_ipapi(current_ip)
            
            # 如果主要API失败，尝试备用API
            if not result.get("success"):
                backup_result = await query_ip_location_ipinfo(current_ip)
                if backup_result.get("success"):
                    result = backup_result
            
            return f"🔍 当前公网IP查询结果\n\n{format_location_info(result)}"
            
    except Exception as e:
        return f"❌ 获取当前IP失败: {str(e)}"

if __name__ == "__main__":
    # 以标准 I/O 方式运行 MCP 服务器
    mcp.run(transport="stdio")
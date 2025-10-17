import os
import json
import platform
import psutil
from datetime import datetime
from typing import Any
from mcp.server.fastmcp import FastMCP

# 初始化 MCP 服务器
mcp = FastMCP("SystemInfoServer")

def get_system_info() -> dict[str, Any]:
    """
    获取本地操作系统的详细软硬件信息。
    :return: 包含系统信息的字典
    """
    try:
        # 系统基本信息
        system_info = {
            "platform": {
                "system": platform.system(),
                "release": platform.release(),
                "version": platform.version(),
                "platform": platform.platform(),
                "architecture": platform.architecture()[0],
                "machine": platform.machine(),
                "processor": platform.processor(),
            },
            "python": {
                "version": platform.python_version(),
                "implementation": platform.python_implementation(),
                "compiler": platform.python_compiler(),
            },
            "cpu": {
                "physical_cores": psutil.cpu_count(logical=False),
                "total_cores": psutil.cpu_count(logical=True),
                "max_frequency": f"{psutil.cpu_freq().current:.2f} MHz" if psutil.cpu_freq() else "N/A",
                "usage_percent": f"{psutil.cpu_percent(interval=1)}%",
            },
            "memory": {
                "total": f"{psutil.virtual_memory().total / (1024**3):.2f} GB",
                "available": f"{psutil.virtual_memory().available / (1024**3):.2f} GB",
                "used": f"{psutil.virtual_memory().used / (1024**3):.2f} GB",
                "usage_percent": f"{psutil.virtual_memory().percent}%",
            },
            "disk": {},
            "network": {},
        }

        # 磁盘信息
        disk_partitions = psutil.disk_partitions()
        for partition in disk_partitions:
            try:
                partition_usage = psutil.disk_usage(partition.mountpoint)
                system_info["disk"][partition.device] = {
                    "mountpoint": partition.mountpoint,
                    "fstype": partition.fstype,
                    "total_size": f"{partition_usage.total / (1024**3):.2f} GB",
                    "used": f"{partition_usage.used / (1024**3):.2f} GB",
                    "free": f"{partition_usage.free / (1024**3):.2f} GB",
                    "usage_percent": f"{partition_usage.percent}%",
                }
            except PermissionError:
                # 有些分区可能无法访问
                continue

        # 网络信息
        net_io = psutil.net_io_counters()
        system_info["network"] = {
            "bytes_sent": f"{net_io.bytes_sent / (1024**2):.2f} MB",
            "bytes_recv": f"{net_io.bytes_recv / (1024**2):.2f} MB",
            "packets_sent": net_io.packets_sent,
            "packets_recv": net_io.packets_recv,
        }

        # 启动时间
        boot_time = psutil.boot_time()
        system_info["boot_time"] = f"{datetime.fromtimestamp(boot_time).strftime('%Y-%m-%d %H:%M:%S')}"

        return system_info

    except Exception as e:
        return {"error": f"获取系统信息时出错: {str(e)}"}

def format_system_info(data: dict[str, Any]) -> str:
    """
    将系统信息格式化为易读文本。
    :param data: 系统信息字典
    :return: 格式化后的系统信息字符串
    """
    if "error" in data:
        return f"⚠️ {data['error']}"

    try:
        output = "🖥️ 系统信息概览\n\n"
        
        # 平台信息
        platform_info = data["platform"]
        output += "📋 操作系统信息:\n"
        output += f"  系统: {platform_info['system']} {platform_info['release']}\n"
        output += f"  版本: {platform_info['version']}\n"
        output += f"  平台: {platform_info['platform']}\n"
        output += f"  架构: {platform_info['architecture']}\n"
        output += f"  处理器: {platform_info['processor']}\n\n"

        # Python 信息
        python_info = data["python"]
        output += "🐍 Python 环境:\n"
        output += f"  版本: {python_info['version']}\n"
        output += f"  实现: {python_info['implementation']}\n"
        output += f"  编译器: {python_info['compiler']}\n\n"

        # CPU 信息
        cpu_info = data["cpu"]
        output += "⚡ CPU 信息:\n"
        output += f"  物理核心: {cpu_info['physical_cores']}\n"
        output += f"  逻辑核心: {cpu_info['total_cores']}\n"
        output += f"  最大频率: {cpu_info['max_frequency']}\n"
        output += f"  当前使用率: {cpu_info['usage_percent']}\n\n"

        # 内存信息
        memory_info = data["memory"]
        output += "💾 内存信息:\n"
        output += f"  总内存: {memory_info['total']}\n"
        output += f"  可用内存: {memory_info['available']}\n"
        output += f"  已使用: {memory_info['used']}\n"
        output += f"  使用率: {memory_info['usage_percent']}\n\n"

        # 磁盘信息
        disk_info = data["disk"]
        output += "💿 磁盘信息:\n"
        for device, info in disk_info.items():
            output += f"  {device} ({info['fstype']}):\n"
            output += f"    挂载点: {info['mountpoint']}\n"
            output += f"    总大小: {info['total_size']}\n"
            output += f"    已使用: {info['used']} ({info['usage_percent']})\n"
            output += f"    可用空间: {info['free']}\n"

        # 网络信息
        network_info = data["network"]
        output += "\n🌐 网络信息:\n"
        output += f"  发送: {network_info['bytes_sent']}\n"
        output += f"  接收: {network_info['bytes_recv']}\n"

        # 启动时间
        output += f"\n⏰ 系统启动时间: {data['boot_time']}"

        return output

    except Exception as e:
        return f"格式化系统信息时出错: {str(e)}"

@mcp.tool()
async def get_system_information() -> str:
    """
    获取本地操作系统的详细软硬件信息。
    
    功能说明:
    - 获取操作系统版本、架构等基本信息
    - 获取 CPU 核心数、频率、使用率
    - 获取内存总量、使用情况
    - 获取磁盘分区和使用情况
    - 获取网络统计信息
    - 获取系统启动时间
    
    :return: 格式化的系统信息报告
    """
    data = get_system_info()
    return format_system_info(data)

if __name__ == "__main__":
    # 以标准 I/O 方式运行 MCP 服务器
    mcp.run(transport="stdio")
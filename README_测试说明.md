# 域名信息查询服务测试说明

## 📋 概述

本项目包含了域名信息查询服务的完整测试套件，专门用于测试 `getDomainInfo_server.py` 服务的各项功能。

## 🚀 快速开始

### 1. 安装依赖

```bash
pip install -r requirements.txt
```

### 2. 运行快速测试（推荐）

```bash
python run_domain_test.py
```

这个脚本会测试 `www.baidu.com` 域名的所有查询功能，包括：
- 单个域名查询
- 批量域名查询
- 域名可用性检查

### 3. 运行完整测试套件

```bash
python test/test_domain_info.py
```

这个脚本提供更详细的测试，包括：
- 完整的测试报告
- 详细的错误信息
- 测试结果保存到 JSON 文件

## 📁 文件说明

### 测试文件

- **`run_domain_test.py`** - 快速测试脚本，简单易用
- **`test/test_domain_info.py`** - 完整测试套件，功能全面

### 服务文件

- **`mcp_servers/getDomainInfo_server.py`** - 域名信息查询服务主文件

## 🔧 测试功能

### 1. 单个域名查询 (`query_domain`)

测试查询单个域名的详细信息：

```python
result = await query_domain("www.baidu.com")
```

**返回信息包括：**
- 域名注册状态
- 注册商信息
- 创建时间和过期时间
- 域名状态
- DNS 服务器信息

### 2. 批量域名查询 (`batch_query_domains`)

测试同时查询多个域名：

```python
result = await batch_query_domains("www.baidu.com,www.google.com")
```

**功能特点：**
- 支持逗号分隔的域名列表
- 返回汇总报告
- 显示查询域名总数

### 3. 域名可用性检查 (`check_domain_availability`)

测试快速检查域名是否可注册：

```python
result = await check_domain_availability("www.baidu.com")
```

**返回结果：**
- 域名可用性状态
- 如果已注册，显示注册商和过期时间
- 提供注册建议

## 📊 测试结果示例

### 成功的测试输出示例：

```
🌐 域名信息查询服务测试
==================================================
测试域名: www.baidu.com
测试时间: 2025-10-17 13:00:00

📋 测试 1: 单个域名查询
------------------------------
🌐 域名查询结果: www.baidu.com

📊 基本信息:
  ✅ 注册状态: 已注册
  🏢 注册商: MarkMonitor Inc.
  📅 创建时间: 1999-10-11
  ⏰ 过期时间: 2026-10-11

🔒 域名状态:
  • clientDeleteProhibited
  • clientTransferProhibited
  • clientUpdateProhibited

🌍 域名服务器:
  • ns1.baidu.com
  • ns2.baidu.com
  • ns3.baidu.com
  • ns4.baidu.com

⏱️ 查询时间: 2025-10-17T13:00:00

✅ 单个域名查询测试通过
```

## 🛠️ 故障排除

### 常见问题

1. **导入模块失败**
   ```
   ❌ 导入模块失败: No module named 'whois'
   ```
   **解决方案：** 安装所需依赖
   ```bash
   pip install -r requirements.txt
   ```

2. **网络连接问题**
   ```
   ❌ 域名查询失败: [Errno 11001] getaddrinfo failed
   ```
   **解决方案：** 检查网络连接，确保可以访问 WHOIS 服务器

3. **权限问题**
   ```
   ❌ 测试执行出错: Permission denied
   ```
   **解决方案：** 确保脚本有执行权限
   ```bash
   chmod +x run_domain_test.py
   ```

### 调试模式

如果测试失败，可以查看详细的错误信息：

1. 运行完整测试套件获取详细报告
2. 检查生成的 `test_report_*.json` 文件
3. 查看控制台输出的具体错误信息

## 📈 性能说明

- **单个域名查询**：通常需要 1-3 秒
- **批量查询**：每个域名约 1-3 秒，串行执行
- **网络依赖**：需要稳定的网络连接访问 WHOIS 服务器

## 🔍 测试覆盖范围

### 功能测试
- ✅ 基础域名信息获取
- ✅ 数据格式化
- ✅ 单个域名查询工具
- ✅ 批量域名查询工具
- ✅ 域名可用性检查工具

### 错误处理测试
- ✅ 网络错误处理
- ✅ 无效域名处理
- ✅ 超时处理
- ✅ 数据解析错误处理

## 📝 自定义测试

您可以修改测试脚本来测试其他域名：

```python
# 在 run_domain_test.py 中修改
domain = "your-domain.com"  # 替换为您要测试的域名
```

或者在批量测试中添加更多域名：

```python
batch_domains = "domain1.com,domain2.com,domain3.com"
```

## 📞 支持

如果您在使用过程中遇到问题，请检查：

1. 网络连接是否正常
2. 依赖包是否正确安装
3. Python 版本是否兼容（推荐 Python 3.8+）
4. 域名格式是否正确

---

**注意：** 由于 WHOIS 查询依赖于外部服务器，测试结果可能会因网络状况和 WHOIS 服务器的可用性而有所不同。
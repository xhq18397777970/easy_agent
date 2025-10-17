#!/usr/bin/env python3
"""
域名信息查询服务测试脚本
测试 getDomainInfo_server.py 的各个功能
"""

import asyncio
import sys
import os
import json
from datetime import datetime

# 添加父目录到 Python 路径，以便导入 MCP 服务器模块
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from mcp_servers.getDomainInfo_server import (
    fetch_domain_info,
    format_domain_info,
    query_domain,
    batch_query_domains,
    check_domain_availability
)


class DomainInfoTester:
    """域名信息查询测试类"""
    
    def __init__(self):
        self.test_results = []
        self.start_time = datetime.now()
    
    def log_test(self, test_name: str, success: bool, message: str = "", data: any = None):
        """记录测试结果"""
        result = {
            'test_name': test_name,
            'success': success,
            'message': message,
            'timestamp': datetime.now().isoformat(),
            'data': data
        }
        self.test_results.append(result)
        
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{status} {test_name}")
        if message:
            print(f"    {message}")
        print()
    
    def test_fetch_domain_info(self, domain: str = "www.baidu.com"):
        """测试基础域名信息获取功能"""
        print(f"🔍 测试基础域名信息获取: {domain}")
        
        try:
            result = fetch_domain_info(domain)
            
            # 检查返回数据结构
            required_keys = ['domain', 'is_registered', 'query_time']
            missing_keys = [key for key in required_keys if key not in result]
            
            if missing_keys:
                self.log_test(
                    "fetch_domain_info", 
                    False, 
                    f"缺少必要字段: {missing_keys}"
                )
                return False
            
            # 检查是否有错误
            if 'error' in result:
                self.log_test(
                    "fetch_domain_info", 
                    False, 
                    f"查询出错: {result['error']}"
                )
                return False
            
            self.log_test(
                "fetch_domain_info", 
                True, 
                f"成功获取域名信息，注册状态: {result['is_registered']}",
                result
            )
            return True
            
        except Exception as e:
            self.log_test(
                "fetch_domain_info", 
                False, 
                f"异常: {str(e)}"
            )
            return False
    
    def test_format_domain_info(self, domain: str = "www.baidu.com"):
        """测试域名信息格式化功能"""
        print(f"📝 测试域名信息格式化: {domain}")
        
        try:
            # 先获取原始数据
            raw_data = fetch_domain_info(domain)
            
            # 格式化数据
            formatted_result = format_domain_info(raw_data)
            
            # 检查格式化结果
            if not formatted_result or len(formatted_result.strip()) == 0:
                self.log_test(
                    "format_domain_info", 
                    False, 
                    "格式化结果为空"
                )
                return False
            
            # 检查是否包含关键信息
            key_indicators = ["域名查询结果", "基本信息", "查询时间"]
            missing_indicators = [ind for ind in key_indicators if ind not in formatted_result]
            
            if missing_indicators:
                self.log_test(
                    "format_domain_info", 
                    False, 
                    f"格式化结果缺少关键信息: {missing_indicators}"
                )
                return False
            
            self.log_test(
                "format_domain_info", 
                True, 
                "成功格式化域名信息",
                {"formatted_length": len(formatted_result)}
            )
            
            # 打印格式化结果的前几行作为示例
            lines = formatted_result.split('\n')[:8]
            print("    格式化结果预览:")
            for line in lines:
                print(f"    {line}")
            print("    ...")
            print()
            
            return True
            
        except Exception as e:
            self.log_test(
                "format_domain_info", 
                False, 
                f"异常: {str(e)}"
            )
            return False
    
    async def test_query_domain(self, domain: str = "www.baidu.com"):
        """测试单个域名查询工具"""
        print(f"🌐 测试单个域名查询工具: {domain}")
        
        try:
            result = await query_domain(domain)
            
            if not result or len(result.strip()) == 0:
                self.log_test(
                    "query_domain", 
                    False, 
                    "查询结果为空"
                )
                return False
            
            # 检查是否包含错误信息
            if "域名查询失败" in result:
                self.log_test(
                    "query_domain", 
                    False, 
                    "域名查询失败"
                )
                return False
            
            self.log_test(
                "query_domain", 
                True, 
                "成功查询域名信息",
                {"result_length": len(result)}
            )
            
            # 打印查询结果的前几行
            lines = result.split('\n')[:6]
            print("    查询结果预览:")
            for line in lines:
                print(f"    {line}")
            print("    ...")
            print()
            
            return True
            
        except Exception as e:
            self.log_test(
                "query_domain", 
                False, 
                f"异常: {str(e)}"
            )
            return False
    
    async def test_batch_query_domains(self, domains: str = "www.baidu.com,www.google.com"):
        """测试批量域名查询工具"""
        print(f"📊 测试批量域名查询工具: {domains}")
        
        try:
            result = await batch_query_domains(domains)
            
            if not result or len(result.strip()) == 0:
                self.log_test(
                    "batch_query_domains", 
                    False, 
                    "批量查询结果为空"
                )
                return False
            
            # 检查是否包含批量查询的关键信息
            if "批量域名查询结果汇总" not in result:
                self.log_test(
                    "batch_query_domains", 
                    False, 
                    "批量查询结果格式不正确"
                )
                return False
            
            domain_count = len(domains.split(','))
            if f"共 {domain_count} 个域名" not in result:
                self.log_test(
                    "batch_query_domains", 
                    False, 
                    "域名数量统计不正确"
                )
                return False
            
            self.log_test(
                "batch_query_domains", 
                True, 
                f"成功批量查询 {domain_count} 个域名",
                {"result_length": len(result)}
            )
            
            # 打印批量查询结果的前几行
            lines = result.split('\n')[:10]
            print("    批量查询结果预览:")
            for line in lines:
                print(f"    {line}")
            print("    ...")
            print()
            
            return True
            
        except Exception as e:
            self.log_test(
                "batch_query_domains", 
                False, 
                f"异常: {str(e)}"
            )
            return False
    
    async def test_check_domain_availability(self, domain: str = "www.baidu.com"):
        """测试域名可用性检查工具"""
        print(f"🔍 测试域名可用性检查工具: {domain}")
        
        try:
            result = await check_domain_availability(domain)
            
            if not result or len(result.strip()) == 0:
                self.log_test(
                    "check_domain_availability", 
                    False, 
                    "可用性检查结果为空"
                )
                return False
            
            # 检查结果是否包含可用性信息
            availability_indicators = ["域名可用", "域名不可用"]
            has_availability_info = any(ind in result for ind in availability_indicators)
            
            if not has_availability_info:
                self.log_test(
                    "check_domain_availability", 
                    False, 
                    "可用性检查结果不包含可用性信息"
                )
                return False
            
            # 判断域名状态
            is_available = "域名可用" in result
            status = "可用" if is_available else "不可用"
            
            self.log_test(
                "check_domain_availability", 
                True, 
                f"成功检查域名可用性，状态: {status}",
                {"is_available": is_available}
            )
            
            # 打印可用性检查结果
            lines = result.split('\n')[:8]
            print("    可用性检查结果:")
            for line in lines:
                print(f"    {line}")
            print()
            
            return True
            
        except Exception as e:
            self.log_test(
                "check_domain_availability", 
                False, 
                f"异常: {str(e)}"
            )
            return False
    
    async def run_all_tests(self):
        """运行所有测试"""
        print("🚀 开始运行域名信息查询服务测试")
        print("=" * 60)
        print()
        
        # 测试域名
        test_domain = "www.baidu.com"
        batch_domains = "www.baidu.com,www.google.com"
        
        # 运行各项测试
        tests = [
            ("基础域名信息获取", self.test_fetch_domain_info, test_domain),
            ("域名信息格式化", self.test_format_domain_info, test_domain),
            ("单个域名查询工具", self.test_query_domain, test_domain),
            ("批量域名查询工具", self.test_batch_query_domains, batch_domains),
            ("域名可用性检查工具", self.test_check_domain_availability, test_domain),
        ]
        
        for test_name, test_func, test_param in tests:
            try:
                if asyncio.iscoroutinefunction(test_func):
                    await test_func(test_param)
                else:
                    test_func(test_param)
            except Exception as e:
                self.log_test(test_name, False, f"测试执行异常: {str(e)}")
        
        # 生成测试报告
        self.generate_test_report()
    
    def generate_test_report(self):
        """生成测试报告"""
        print("=" * 60)
        print("📋 测试报告")
        print("=" * 60)
        
        total_tests = len(self.test_results)
        passed_tests = sum(1 for result in self.test_results if result['success'])
        failed_tests = total_tests - passed_tests
        
        print(f"总测试数: {total_tests}")
        print(f"通过测试: {passed_tests}")
        print(f"失败测试: {failed_tests}")
        print(f"成功率: {(passed_tests/total_tests*100):.1f}%")
        print()
        
        # 显示失败的测试
        if failed_tests > 0:
            print("❌ 失败的测试:")
            for result in self.test_results:
                if not result['success']:
                    print(f"  - {result['test_name']}: {result['message']}")
            print()
        
        # 计算测试耗时
        end_time = datetime.now()
        duration = (end_time - self.start_time).total_seconds()
        print(f"测试耗时: {duration:.2f} 秒")
        
        # 保存详细测试结果到文件
        report_file = f"test_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(report_file, 'w', encoding='utf-8') as f:
            json.dump({
                'summary': {
                    'total_tests': total_tests,
                    'passed_tests': passed_tests,
                    'failed_tests': failed_tests,
                    'success_rate': passed_tests/total_tests*100,
                    'duration_seconds': duration
                },
                'test_results': self.test_results
            }, f, ensure_ascii=False, indent=2)
        
        print(f"详细测试报告已保存到: {report_file}")


async def main():
    """主函数"""
    print("🌐 域名信息查询服务测试脚本")
    print("测试目标: www.baidu.com")
    print()
    
    # 创建测试器并运行测试
    tester = DomainInfoTester()
    await tester.run_all_tests()


if __name__ == "__main__":
    # 运行异步测试
    asyncio.run(main())
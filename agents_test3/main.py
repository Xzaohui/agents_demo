#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
商业数据分析多智能体系统 - 主入口

这个系统实现了一个类似 manus 的多智能体架构，用于商业数据分析。
系统包含三层架构：
1. 工具层：提供各种数据收集和分析工具
2. 智能体层：包括专家智能体、协调智能体和用户交互智能体
3. 控制层：负责整体流程管理和结果整合

使用方法：
    python main.py [分析类型] [类目名称] [开始日期] [结束日期]

示例：
    python main.py 市场趋势 智能手机 2023-01-01 2023-12-31
    python main.py 竞品分析 平板电脑 2023-01-01 2023-12-31
"""

import sys
import time
from datetime import datetime
from business_analysis.system import BusinessAnalysisSystem


def print_banner():
    """
    打印系统横幅
    """
    banner = """
    ____              _                       _                _           _     
   |  _ \            (_)                     | |              | |         (_)    
   | |_) |_   _  ___  _  _ __    ___  ___ ___| |     __ _ _ __| |_   _ ___ _ ___ 
   |  _ <| | | |/ __|| || '_ \  / _ \/ __/ __| |    / _` | '__| | | | / __| / __|
   | |_) | |_| | (__ | || | | ||  __/\__ \__ \ |___| (_| | |  | | |_| \__ \ \__ \
   |____/ \__,_|\___||_||_| |_| \___||___/___/______\__,_|_|  |_|\__, |___/_|___/
                                                                  __/ |          
                                                                 |___/           
    __  __       _ _   _                            _       _____           _                 
   |  \/  |     | | | (_)                          | |     / ____|         | |                
   | \  / |_   _| | |_ _    __ _  __ _  ___ _ __ | |_   | (___  _   _ ___| |_ ___ _ __ ___  
   | |\/| | | | | | __| |  / _` |/ _` |/ _ \ '_ \| __|   \___ \| | | / __| __/ _ \ '_ ` _ \ 
   | |  | | |_| | | |_| | | (_| | (_| |  __/ | | | |_    ____) | |_| \__ \ ||  __/ | | | | |
   |_|  |_|\__,_|_|\__|_|  \__,_|\__, |\___|_| |_|\__|  |_____/ \__, |___/\__\___|_| |_| |_|
                                   __/ |                          __/ |                      
                                  |___/                          |___/                       
    """
    print(banner)
    print("\n商业数据分析多智能体系统 v1.0")
    print("="*80)


def print_help():
    """
    打印帮助信息
    """
    print("\n使用方法:")
    print("    python main.py [分析类型] [类目名称] [开始日期] [结束日期]\n")
    print("支持的分析类型:")
    print("    市场趋势 - 分析市场整体趋势、季节性和增长率")
    print("    竞品分析 - 分析竞争对手情况、差距和机会")
    print("\n示例:")
    print("    python main.py 市场趋势 智能手机 2023-01-01 2023-12-31")
    print("    python main.py 竞品分析 平板电脑 2023-01-01 2023-12-31")


def validate_date(date_str):
    """
    验证日期格式是否正确
    
    Args:
        date_str: 日期字符串，格式应为YYYY-MM-DD
        
    Returns:
        如果格式正确则返回True，否则返回False
    """
    try:
        datetime.strptime(date_str, "%Y-%m-%d")
        return True
    except ValueError:
        return False


def main():
    """
    主函数
    """
    print_banner()
    
    # 检查命令行参数
    if len(sys.argv) < 5 or sys.argv[1] in ["-h", "--help"]:
        print_help()
        return
    
    analysis_type = sys.argv[1]
    category = sys.argv[2]
    start_date = sys.argv[3]
    end_date = sys.argv[4]
    
    # 验证分析类型
    if analysis_type not in ["市场趋势", "竞品分析"]:
        print(f"错误: 不支持的分析类型 '{analysis_type}'")
        print("支持的分析类型: 市场趋势, 竞品分析")
        return
    
    # 验证日期格式
    if not validate_date(start_date) or not validate_date(end_date):
        print("错误: 日期格式不正确，应为YYYY-MM-DD格式")
        return
    
    # 创建分析请求
    analysis_request = {
        'analysis_type': analysis_type,
        'category': category,
        'time_range': {
            'start_date': start_date,
            'end_date': end_date
        },
        'additional_parameters': {
            'focus_competitors': ['CompA', 'CompB', 'CompC'],
            'key_metrics': ['sales', 'market_share', 'growth_rate']
        }
    }
    
    # 创建系统实例
    print(f"\n初始化商业数据分析系统...")
    system = BusinessAnalysisSystem()
    
    # 提交分析请求
    user_id = "user_" + str(int(time.time()))
    print(f"提交{analysis_type}分析请求: 类目={category}, 时间范围={start_date}至{end_date}")
    request_id = system.submit_analysis_request(user_id, analysis_request)
    print(f"请求已提交，请求ID: {request_id}")
    
    # 运行系统并显示进度
    print("\n开始分析处理...")
    total_steps = 20
    for step in range(1, total_steps + 1):
        # 显示进度条
        progress = int(step / total_steps * 50)
        sys.stdout.write("\r处理进度: [" + "#" * progress + " " * (50 - progress) + "] " + str(int(step / total_steps * 100)) + "%")
        sys.stdout.flush()
        
        # 运行一步
        system.run_step()
        time.sleep(0.2)  # 模拟处理时间
    
    print("\n\n分析完成!")
    
    # 获取请求状态
    status = system.get_request_status(request_id)
    print(f"请求状态: {status['status']}")
    
    # 在实际系统中，这里会显示分析报告的详细内容
    print("\n分析报告摘要:")
    print("-" * 80)
    if analysis_type == "市场趋势":
        print(f"类目 '{category}' 在 {start_date} 至 {end_date} 期间的市场趋势分析")
        print("\n主要发现:")
        print("1. 市场整体呈现稳定增长趋势，年增长率约为5.3%")
        print("2. 销售呈现明显的季节性，Q4销售占比最高，达到35%")
        print("3. 相对市场增长率，产品增长率高出2.1个百分点，表现良好")
        print("\n主要洞察:")
        print("1. 建议在Q3末增加库存，为Q4销售高峰做准备")
        print("2. 线上渠道增长迅速，建议加大线上营销投入")
        print("3. 年轻消费者群体需求增长迅速，可考虑开发针对性产品")
    else:  # 竞品分析
        print(f"类目 '{category}' 在 {start_date} 至 {end_date} 期间的竞品分析")
        print("\n主要发现:")
        print("1. 主要竞争对手市场份额: CompA(25%), CompB(18%), CompC(12%)")
        print("2. 产品在质量和用户体验方面具有优势，但价格竞争力较弱")
        print("3. 竞争对手CompB在技术创新方面投入加大，可能构成威胁")
        print("\n主要洞察:")
        print("1. 建议优化成本结构，提高价格竞争力")
        print("2. 加强产品质量和用户体验优势的市场传播")
        print("3. 关注CompB的技术动向，加大研发投入")
    print("-" * 80)
    
    print("\n完整报告已生成，感谢使用商业数据分析多智能体系统!")


if __name__ == "__main__":
    main()
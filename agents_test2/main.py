import asyncio
from orchestrator import AnalysisOrchestrator

async def main():
    # 创建编排器实例
    orchestrator = AnalysisOrchestrator()
    
    # 运行分析流程
    result = await orchestrator.run_analysis(
        category="智能手机",
        start_date="2025-01-01",
        end_date="2025-03-31"
    )
    
    # 打印结果
    if result["success"]:
        print("分析完成！")
        print("\n=== 报告摘要 ===")
        report = result["data"]["report"]
        print(f"标题: {report['title']}")
        print(f"总结: {report['summary']}")
        
        print("\n市场洞察:")
        for insight in report["market_insights"]:
            print(f"- {insight}")
        
        print("\n趋势洞察:")
        for insight in report["trend_insights"]:
            print(f"- {insight}")
        
        print("\n建议:")
        for recommendation in report["recommendations"]:
            print(f"- {recommendation}")
    else:
        print(f"分析失败: {result['message']}")

if __name__ == "__main__":
    asyncio.run(main())

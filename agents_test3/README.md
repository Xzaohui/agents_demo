# 商业数据分析多智能体系统

## 项目概述

这是一个基于多智能体架构的商业数据分析系统，设计用于处理复杂的商业数据分析任务。系统采用类似 manus 的多智能体架构，通过智能体之间的协作完成数据收集、分析和洞察生成。

## 系统架构

系统采用三层架构设计：

### 1. 工具层

提供各种数据收集和分析工具，包括：

- **数据收集工具**：获取市场数据、销售数据、竞品数据、产品数据等
- **数据分析工具**：趋势分析、季节性分析、对比分析、差距分析等
- **洞察生成工具**：生成趋势洞察、机会洞察、风险洞察、竞争优势洞察等

### 2. 智能体层

包含多种专业化的智能体，各司其职：

- **协调智能体**：负责任务分解、分配和监控，是系统的中央协调者
- **专家智能体**：负责特定领域的分析任务，如市场数据专家、销售数据专家等
- **用户交互智能体**：负责与用户进行交互，接收用户请求并返回分析结果

### 3. 控制层

负责整体流程管理和结果整合：

- **消息处理系统**：实现智能体之间的通信
- **系统控制器**：管理系统运行流程，协调各智能体工作

## 工作流程

1. **任务接收**：用户交互智能体接收用户的分析请求
2. **任务分解**：协调智能体将复杂任务分解为子任务
3. **任务分配**：协调智能体根据专业领域将子任务分配给专家智能体
4. **数据收集**：专家智能体使用数据收集工具获取所需数据
5. **数据分析**：专家智能体使用分析工具处理数据
6. **洞察生成**：专家智能体生成业务洞察
7. **结果整合**：协调智能体整合各专家智能体的分析结果
8. **报告生成**：协调智能体生成最终分析报告
9. **结果返回**：用户交互智能体将分析报告返回给用户

## 智能体通信机制

智能体之间通过消息传递机制进行通信，消息包含以下要素：

- 消息ID
- 发送者ID
- 接收者ID
- 消息类型
- 消息内容
- 引用消息ID（可选）
- 时间戳

## 主要功能

系统支持多种商业数据分析任务，包括但不限于：

- **市场趋势分析**：分析市场整体趋势、季节性和增长率
- **竞品分析**：分析竞争对手情况、差距和机会

## 使用方法

### 命令行使用

```bash
python main.py [分析类型] [类目名称] [开始日期] [结束日期]
```

示例：

```bash
python main.py 市场趋势 智能手机 2023-01-01 2023-12-31
python main.py 竞品分析 平板电脑 2023-01-01 2023-12-31
```

### 编程接口使用

```python
from business_analysis.system import BusinessAnalysisSystem

# 创建系统实例
system = BusinessAnalysisSystem()

# 创建分析请求
analysis_request = {
    'analysis_type': '市场趋势',
    'category': '智能手机',
    'time_range': {
        'start_date': '2023-01-01',
        'end_date': '2023-12-31'
    },
    'additional_parameters': {
        'focus_competitors': ['CompA', 'CompB', 'CompC'],
        'key_metrics': ['sales', 'market_share', 'growth_rate']
    }
}

# 提交分析请求
user_id = "user_123"
request_id = system.submit_analysis_request(user_id, analysis_request)

# 运行系统
system.run(steps=20)

# 获取请求状态
status = system.get_request_status(request_id)
```

## 系统扩展

系统设计具有高度的可扩展性：

1. **添加新工具**：可以通过实现新的工具类来扩展系统功能
2. **添加新智能体**：可以创建新的专家智能体来处理特定领域的任务
3. **支持新分析类型**：可以在协调智能体中添加新的任务分解逻辑来支持新的分析类型

## 项目结构

```python
business_analysis/
├── __init__.py
├── agents/
│   ├── __init__.py
│   ├── base_agent.py        # 基础智能体类
│   ├── coordinator_agent.py # 协调智能体类
│   ├── expert_agent.py      # 专家智能体类
│   └── user_interface_agent.py # 用户交互智能体类
├── models/
│   ├── __init__.py
│   └── message.py           # 消息模型
├── tools/
│   ├── __init__.py
│   ├── data_collection_tools.py    # 数据收集工具
│   ├── data_analysis_tools.py       # 数据分析工具
│   └── insight_generation_tools.py  # 洞察生成工具
├── messaging/
│   ├── __init__.py
│   └── message_handler.py   # 消息处理器
└── system.py               # 系统主类
main.py                     # 主入口文件
```

## 注意事项

- 当前版本中的数据工具返回的是模拟数据，实际使用时需要连接到真实的数据源
- 系统运行需要Python 3.6+环境
- 系统设计遵循模块化原则，各组件之间通过明确的接口进行交互，便于维护和扩展
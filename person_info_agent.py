import json
from dataclasses import asdict

from smolagents import (
    CodeAgent,
    OpenAIServerModel,
    tool,
    PromptTemplates,
    PlanningPromptTemplate,
    ManagedAgentPromptTemplate,
    FinalAnswerPromptTemplate,
)

# 假设你的配置加载类 utils.py 在这里
# from utils import GeneralConfig, PromptConfig
# 为了让代码可直接运行，我将在这里重新定义这些类
from utils import GeneralConfig, PromptConfig  # 请确保这里的导入路径正确


# 1. 加载通用配置和为新任务定制的Prompt配置
# =================================================
general_config = GeneralConfig.load_from_yaml(
    "configs/general_configs/agent_config.yaml"
)
# 注意：这里加载的是我们新创建的YAML文件
prompt_config = PromptConfig.load_from_yaml(
    "configs/prompt_configs/person_info_prompts.yaml"
)


# 2. 初始化模型 (与之前相同)
# =================================================
model = OpenAIServerModel(
    model_id="deepseek-chat",
    api_base=general_config.Agent.base_url,
    api_key=general_config.Agent.api_key,
)


# 3. 定义新任务所需的工具
# =================================================
@tool
def get_person_info(names: list[str]) -> str:
    """
    根据输入的姓名列表，查询每个人的个人信息（年龄和城市）。
    能处理部分姓名查询失败的情况。

    Args:
        names: 待查询信息的人的姓名列表
    """
    # 模拟一个信息数据库
    db = {
        "张三": {"age": 30, "city": "北京"},
        "李四": {"age": 25, "city": "上海"},
    }

    results = {}
    for name in names:
        # 使用 .get() 方法优雅地处理未找到的情况
        results[name] = db.get(name, "未找到")

    # 返回一个JSON字符串，这是最健壮的方式
    return json.dumps(results, ensure_ascii=False)


# 4. 使用加载的配置，以最佳实践方式初始化Prompt模板
# =================================================
# 注意：这里我们使用 **asdict(...) 的方式来解包，这是最简洁和健壮的
prompt_templates = PromptTemplates(
    system_prompt=prompt_config.system_prompt,
    planning=PlanningPromptTemplate(prompt_config.planning_prompt.to_dict()),
    managed_agent=ManagedAgentPromptTemplate(
        prompt_config.managed_agent_prompt.to_dict()
    ),
    final_answer=FinalAnswerPromptTemplate(prompt_config.final_answer_prompt.to_dict()),
)


# 5. 创建并配置Agent实例
# =================================================
agent = CodeAgent(
    tools=[get_person_info],  # 传入新定义的工具
    model=model,
    # prompt_templates=prompt_templates,  # 传入为新任务定制的Prompt
)


# 6. 定义一个包含成功和失败案例的测试任务并运行
# =================================================
user_task = "请帮我查询张三、李四的个人信息，并整理好结果告诉我。"

print(f"--- Starting Agent with Task ---\n'{user_task}'\n")
result = agent.run(user_task)

print("\n--- Final Answer from Agent ---")
print(result)

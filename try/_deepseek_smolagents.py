import json

from smolagents import (
    CodeAgent,
    InferenceClientModel,
    OpenAIServerModel,
    tool,
    PromptTemplates,
    PlanningPromptTemplate,
    ManagedAgentPromptTemplate,
    FinalAnswerPromptTemplate,
)

from utils import GeneralConfig, PromptConfig


general_config = GeneralConfig.load_from_yaml("configs/general_configs/agent_config.yaml")
prompt_config = PromptConfig.load_from_yaml("configs/prompt_configs/prompt_config_test.yaml")

# Initialize a model (using Hugging Face Inference API)
model = InferenceClientModel()  # Uses a default model
model = OpenAIServerModel(
    model_id="deepseek-chat",
    api_base=general_config.Agent.base_url,
    api_key=general_config.Agent.api_key,
)


@tool
def get_singers(songs: list[str]) -> str:
    """
    该工具可以根据输入的歌名列表，一次性获取所有对应的歌手。
    Args:
        songs: list[str]: 包含多个歌曲名称的列表。
    Return:
        一个JSON格式的字符串，其中key是歌曲名，value是歌手名或'未知'。
    """
    results = {}
    for song in songs:
        if song == "我只在乎你":
            results[song] = "邓丽君"
        elif song == "Metropolis":
            results[song] = "Dream Theater"
        else:
            results[song] = "未知"  # 使用统一的标识
    return json.dumps(results, ensure_ascii=False)  # 保证返回的是一个字符串


prompt_template = PromptTemplates(
    system_prompt="test",
    planning=PlanningPromptTemplate(prompt_config.planning_prompt.to_dict()),
    managed_agent=ManagedAgentPromptTemplate(prompt_config.managed_agent_prompt.to_dict()),
    final_answer=FinalAnswerPromptTemplate(prompt_config.final_answer_prompt.to_dict()),
)


# Create an agent with no tools
agent = CodeAgent(tools=[get_singers], model=model)

# Run the agent with a task
result = agent.run(
    "我想知道'我只在乎你''Metropolis''平凡之路'这几首歌是谁的。请调用工具并使用final_answer返回歌手的名字，不要进行print，如果有某首歌未找到答案，也当作找到，正常进行final_answer，最好请在给出答案前将答案组织成人类可读的形式"
)
print(result)

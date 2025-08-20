import asyncio

from agents import Agent, Runner, set_default_openai_client, set_default_openai_api, set_tracing_disabled, function_tool
from openai import AsyncOpenAI


# 创建DeepSeek客户端
client = AsyncOpenAI(
    api_key="sk-xxxxxxxxxx", 
    base_url="https://api.deepseek.com"
)

set_default_openai_client(client)
set_default_openai_api("chat_completions")
set_tracing_disabled(True)


@function_tool
def get_poem_writer(poem: str) -> str:
    if poem == "大鹏展翅九万里":
        return "王晓明"
    elif poem == "时而伏卧时而起":
        return "李小虎"
    else:
        return "我不知道"


# 创建Agent时传入自定义客户端
agent = Agent(
    name="DeepSeek Assistant", 
    instructions="你是一个专业陪聊，如果用户日常聊天，则正常回应，如果用户提问某些领域知识，你需要查看工具中有没有适合回复的函数，并调用",
    model="deepseek-chat",
    tools=[get_poem_writer],
)

# 使用示例
if __name__ == "__main__":
    result = Runner.run_sync(
        agent, 
        "我想知道'大鹏展翅九万里''时而伏卧时而起''床前地上一片霜'这三句诗的作者分别是谁"
    )
    print(result.final_output)
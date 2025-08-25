import json

# from agents import Agent, Runner, set_default_openai_client, set_default_openai_api, set_tracing_disabled, function_tool
from openai import OpenAI

from utils import AgentConfig

config = AgentConfig()
config.load_config("configs/general_configs/agent_config.yaml")

# 创建DeepSeek客户端
client = OpenAI(
    api_key=config.api_key, 
    base_url=config.base_url
)

def get_poem_writer(poem: str) -> str:
    if poem == "大鹏展翅九万里":
        return "王晓明"
    elif poem == "时而伏卧时而起":
        return "李小虎"
    else:
        return "我不知道"

def send_messages(messages):
    response = client.chat.completions.create(
        model="deepseek-chat",
        messages=messages,
        tools=tools
    )
    return response.choices[0].message


functions_map = {
    "get_poem_writer": get_poem_writer
}


tools = [
    {
        "type": "function",
        "function": {
            "name": "get_poem_writer",
            "description": "获取诗句的作者",
            "parameters": {
                "type": "object",
                "properties": {
                    "poem": {
                        "type": "string",
                        "description": "诗句内容",
                    }
                },
                "required": ["poem"]
            },
        }
    },
]

# TODO: 设置一个函数字典，用于通过函数名提取函数工具
messages = [{"role": "system", "content": "你是一个查诗句和聊天助手，如果用户发送的请求需要查诗句，则调用工具，否则正常聊天即可"}, {"role": "user", "content": "今天天气不错，我想出去玩，帮我推荐几个北京适合玩的地方吧！以及我今天出去玩的时候看到了几句诗，想让你帮忙查一下作者，分别是'大鹏展翅九万里''时而伏卧时而起''坐地日行八万里'，请先给我推荐北京的游玩地点，再告诉我诗句的作者"}]
completed_message = send_messages(messages)

if completed_message.tool_calls:
    messages.append(json.loads(completed_message.model_dump_json()))
    for tool_call in completed_message.tool_calls:
        function_name = tool_call.function.name
        function_args = json.loads(tool_call.function.arguments)
        writer = functions_map[function_name](**function_args)
        messages.append({"role": "tool", "tool_call_id": tool_call.id, "name": function_name, "content": writer})
    message = send_messages(messages)
    print(f"Model>\t {message.content}")
else:
    print(completed_message.content)
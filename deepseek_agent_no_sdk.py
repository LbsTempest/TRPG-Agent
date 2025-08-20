import json

from agents import Agent, Runner, set_default_openai_client, set_default_openai_api, set_tracing_disabled, function_tool
from openai import OpenAI


# 创建DeepSeek客户端
client = OpenAI(
    api_key="sk-xxxxxxxxxxxxxx", 
    base_url="https://api.deepseek.com"
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
messages = [{"role": "user", "content": "'大鹏展翅九万里'的作者是谁"}]
completed_message = send_messages(messages)
function_call = completed_message.tool_calls[0]
writer = globals()[function_call.function.name](**json.loads(function_call.function.arguments))
messages.append({"role": "tool", "tool_call_id": function_call.id, "content": writer})

print(function_call)

message = send_messages(messages)
print(f"Model>\t {message.content}")

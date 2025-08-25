# Import relevant functionality
# from langchain.chat_models import init_chat_model
from langchain_core.tools import tool
from langchain_deepseek import ChatDeepSeek
from langgraph.checkpoint.memory import MemorySaver
from langgraph.prebuilt import create_react_agent

from utils.configs import GeneralConfig

deepseek_config = GeneralConfig.load_from_yaml("config/agent_config.yaml")


@tool
def get_personal_info(name: str) -> str:
    """
    get personal information based on input name, including age, gender and address
    Args:
        name: person to check
    """
    if name == "zhang":
        return "18 years old, male, beijing"
    elif name == "wang":
        return "21 years old, female, shanghai"
    elif name == "li":
        return "16 years old, female, guangzhou"
    else:
        return "i don't know"


# Create the agent
memory = MemorySaver()
# model = init_chat_model("anthropic:claude-3-5-sonnet-latest")
model = ChatDeepSeek(
    model="deepseek-chat",
    api_key=deepseek_config.Agent.api_key,
    temperature=0,
    max_tokens=None,
    timeout=None,
    max_retries=2,
    # other params...
)

tools = [get_personal_info]
agent_executor = create_react_agent(model, tools, checkpointer=memory)
config = {"configurable": {"thread_id": "abc123"}}
input_message = {
    "role": "user",
    "content": "Hi, i want to know the age of wang, the gender of zhang, and the address of li. all letters are lowercase, step by step.",
}

response = agent_executor.invoke({"messages": [input_message]}, config)

for message in response["messages"]:
    message.pretty_print()

# # stream interaction
# for step in agent_executor.stream(
#     {"messages": [input_message]}, config, stream_mode="values"
# ):
#     step["messages"][-1].pretty_print()

from smolagents import CodeAgent, InferenceClientModel, OpenAIServerModel

from utils import AgentConfig


config = AgentConfig()
config.load_config("config/agent_config.yaml")

# Initialize a model (using Hugging Face Inference API)
model = InferenceClientModel()  # Uses a default model
model = OpenAIServerModel(
    model_id="deepseek-chat",
    api_base=config.base_url,
    api_key=config.api_key
)

# Create an agent with no tools
agent = CodeAgent(tools=[], model=model)

# Run the agent with a task
result = agent.run("Calculate the sum of numbers from 1 to 10")
print(result)
from pydantic import Field
from openai import OpenAI
import instructor
from atomic_agents import AtomicAgent, AgentConfig, BasicChatInputSchema, BaseIOSchema
from atomic_agents.context import SystemPromptGenerator, ChatHistory
from utils import GeneralConfig

# Define a custom output schema
class CustomOutputSchema(BaseIOSchema):
    """
    docstring for the custom output schema
    """

    chat_message: str = Field(..., description="The chat message from the agent.")
    suggested_questions: list[str] = Field(
        ..., description="Suggested follow-up questions."
    )


# Set up the system prompt
system_prompt_generator = SystemPromptGenerator(
    background=[
        "This assistant is knowledgeable, helpful, and suggests follow-up questions."
    ],
    steps=[
        "Analyze the user's input to understand the context and intent.",
        "Formulate a relevant and informative response.",
        "Generate 3 suggested follow-up questions for the user.",
    ],
    output_instructions=[
        "Provide clear and concise information in response to user queries.",
        "Conclude each response with 3 relevant suggested questions for the user.",
    ],
)

general_config = GeneralConfig.load_from_yaml("configs/general_configs/agent_config.yaml")

# Initialize OpenAI client
client = instructor.from_openai(OpenAI(**general_config.Agent.to_dict()))

# Initialize the agent
agent = AtomicAgent[BasicChatInputSchema, CustomOutputSchema](
    config=AgentConfig(
        client=client,
        model="deepseek-chat",
        system_prompt_generator=system_prompt_generator,
        history=ChatHistory(),
    )
)

# Example usage
if __name__ == "__main__":
    user_input = "Tell me about atomic agents framework"
    response = agent.run(BasicChatInputSchema(chat_message=user_input))
    print(f"Agent: {response.chat_message}")
    print("Suggested questions:")
    for question in response.suggested_questions:
        print(f"- {question}")

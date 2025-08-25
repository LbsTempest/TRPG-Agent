import os

from atomic_agents import BaseTool, BaseToolConfig, BaseIOSchema
from pydantic import Field
################
# Input Schema #
################


class MyToolInputSchema(BaseIOSchema):
    """Define what your tool accepts as input"""

    value: str = Field(..., description="Input value to process")


#####################
# Output Schema(s)  #
#####################


class MyToolOutputSchema(BaseIOSchema):
    """Define what your tool returns"""

    result: str = Field(..., description="Processed result")


#################
# Configuration #
#################


class MyToolConfig(BaseToolConfig):
    """Tool configuration options"""

    api_key: str = Field(
        default=os.getenv("MY_TOOL_API_KEY"), description="API key for the service"
    )


#####################
# Main Tool & Logic #
#####################


class MyTool(BaseTool[MyToolInputSchema, MyToolOutputSchema]):
    """Main tool implementation"""

    input_schema = MyToolInputSchema
    output_schema = MyToolOutputSchema

    def __init__(self, config: MyToolConfig = MyToolConfig()):
        super().__init__(config)
        self.api_key = config.api_key

    def run(self, params: MyToolInputSchema) -> MyToolOutputSchema:
        # Implement your tool's logic here
        result = self.process_input(params.value)
        return MyToolOutputSchema(result=result)
    
    def process_input(self, input: str) -> str:
        pass

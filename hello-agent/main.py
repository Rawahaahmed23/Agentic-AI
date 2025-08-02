import os
from dotenv import load_dotenv
from agents import Agent, Runner, AsyncOpenAI, OpenAIChatCompletionsModel,function_tool
from agents.run import RunConfig


load_dotenv()


gemini_api_key = os.getenv("GEMINI_API_KEY")


external_client = AsyncOpenAI(
    api_key=gemini_api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)


model = OpenAIChatCompletionsModel(
    model="gemini-1.5-flash",
    openai_client=external_client
)


@function_tool
def multipy(a:int,b:int)->int:
    """Exact multiplication (use this instead of guessing math)."""
    return a * b


@function_tool
def sum(a:int ,b:int)-> int: 
    return a+b
  
config = RunConfig(
    model=model,
    model_provider=external_client
)


agent = Agent(
    name="Assistant",
    instructions="You are a helpful Assistant.",
    model=model,
     tools=[multipy, sum],  # 🛠️ Register tools here
)


result = Runner.run_sync(agent,  "what is 19 + 23 * 2?", run_config=config)

print(result.final_output)

import os
from dotenv import load_dotenv
from agents import Agent, Runner, AsyncOpenAI, OpenAIChatCompletionsModel
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


config = RunConfig(
    model=model,
    model_provider=external_client
)


agent = Agent(
    name="Assistant",
    instructions="You are a helpful Assistant.",
    model=model
)


result = Runner.run_sync(agent, "Tell me about recursion in programming.", run_config=config)

print(result.final_output)

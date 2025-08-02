import os
from dotenv import load_dotenv
from agents import Agent, Runner, AsyncOpenAI, OpenAIChatCompletionsModel
from agents.run import RunConfig
import asyncio


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
    model_provider=external_client,
    tracing_disabled=True  
)


agent = Agent(
    name="Assistant",
    instructions="You are a helpful Assistant.",
    model=model
)


async def ask(prompt):
    result = await Runner.run(agent, prompt, run_config=config)
    return result.final_output


async def main():
    prompts = [
        "What is recursion?",
        "Explain machine learning in simple terms.",
        "What is the difference between AI and ML?"
    ]


    results = await asyncio.gather(*(ask(p) for p in prompts))

  
    for i, output in enumerate(results):
        print(f"\n🧠 Answer {i+1}:\n{output}\n")


if __name__ == "__main__":
    asyncio.run(main())

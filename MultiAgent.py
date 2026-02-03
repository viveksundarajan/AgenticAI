import asyncio

from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.ui import Console
from autogen_ext.models.openai import OpenAIChatCompletionClient


async def createAgent() :


    openai_model_client  = OpenAIChatCompletionClient( model="gpt-4o-mini",api_key="OPENAI_API_KEY")
    AIassistant = AssistantAgent(name="AIassistant", model_client=openai_model_client)

    await Console(AIassistant.run_stream(task="what is the capital of France?"))
    await openai_model_client.close()


asyncio.run(createAgent())
import asyncio

from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.ui import Console
from autogen_ext.models.openai import OpenAIChatCompletionClient


async def createAgent() :


    openai_model_client  = OpenAIChatCompletionClient( model="gpt-4o-mini",api_key="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")
    AIassistant = AssistantAgent(name="AIassistant", model_client=openai_model_client)

    await Console(AIassistant.run_stream(task="what is the capital of France?"))
    await openai_model_client.close()


asyncio.run(createAgent())
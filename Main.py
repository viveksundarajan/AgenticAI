import asyncio

from autogen_agentchat.teams import RoundRobinGroupChat
from autogen_agentchat.ui import Console
from autogen_ext.models.openai import OpenAIChatCompletionClient

from AgentFactory import AgentFactory
from Base import Base
from Terminate import Terminate


async def main():

    base = Base()
    openai_model_client = OpenAIChatCompletionClient(model= base.get_model_client(),
                                                    api_key=base.get_api_key())
    agent_factory = AgentFactory(openai_model_client)
    jira_assistance = agent_factory.get_jira_agent()
    file_assistance = agent_factory.get_file_agent()
    automation_assistance = agent_factory.get_playwright_agent()

    terminate =Terminate()


    group = RoundRobinGroupChat(participants=[jira_assistance, file_assistance, automation_assistance], termination_condition=terminate.get_text_mention_termination())
    await Console(group.run_stream(task="Jira assistance :"
                                        "1. get the last created user story from the project AIAG"
                                        "2. Design a stable user scenarios for stable smoke tests"
                                        "file assistance :cleary write the automated test scenarios designed by jira assistance to a file in the local filesystem with clear test steps and with generated test case id as user story id for better traceability."
                                         "Automation assistance :"
                                         "Once the test scenario creation completed,automate the test scenarios using playwright mcp tool headed mode which created by file assistant"
                                          "Ignore popups by reject it and Make sure to validate the expected results mentioned in the test scenarios"
                                          "quit the browser once all the test scenarios are automated"
                                   ))
    await openai_model_client.close()

asyncio.run(main())
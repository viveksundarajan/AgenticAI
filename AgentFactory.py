from autogen_agentchat.agents import AssistantAgent

from Base import Base
from MCPInstance import MCPInstance


class AgentFactory:

    def __init__(self, openai_model_client):
        self.openai_model_client = openai_model_client
        self.mcp_instance = MCPInstance()
        self.base = Base()



    def get_jira_agent(self):
        return AssistantAgent(name="JiraAgent", model_client=self.openai_model_client, workbench=self.mcp_instance.get_jira_instance(),
                                         system_message=self.base.get_jira_context())


    def get_file_agent(self):
        return AssistantAgent(name="FileAgent", model_client=self.openai_model_client, workbench=self.mcp_instance.get_file_instance(),
                              system_message=self.base.get_file_context())

    def get_playwright_agent(self):
        return AssistantAgent(name="PlaywrightAgent", model_client=self.openai_model_client, workbench=self.mcp_instance.get_playwright_instance(),
                              system_message=self.base.get_automation_context())

    def get_selenium_agent(self):
        return AssistantAgent(name="SeleniumAgent", model_client=self.openai_model_client,
                              workbench=self.mcp_instance.get_selenium_instance(),
                              system_message="You are selenium Agent connected to a web browser via MCP."
                                             "Your task is to assist with web automation tasks such as navigating web pages, interacting with web elements, and extracting information."
                                             "You can perform actions like clicking buttons, filling out forms, and scraping data from web pages."
                                             "ignore any user centric popups and modals"
                                             "Ensure to handle web selectors correctly and confirm actions before executing them."
                                             "Always provide clear feedback on the success or failure of web automation tasks."
                                             "If you encounter any issues, report them clearly.")

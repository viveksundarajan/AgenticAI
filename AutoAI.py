# import asyncio
# import os
#
# import mcp.shared.session as mcp_session
#
# from autogen_agentchat.agents import AssistantAgent
# from autogen_agentchat.conditions import TextMentionTermination
# from autogen_agentchat.teams import RoundRobinGroupChat
# from autogen_agentchat.ui import Console
# from autogen_ext.models.openai import OpenAIChatCompletionClient
# from autogen_ext.tools.mcp import StdioServerParams, McpWorkbench
#
# os.environ["JIRA_URL"] = "https://viveksvvek.atlassian.net"
# os.environ["JIRA_USERNAME"] = "viveksvvek@gmail.com"
# os.environ["JIRA_API_TOKEN"] = "ATATT3xFfGF0FW4HoaKRYMcf0uUELi_jIFtJ-9oKbf5rm8pctwQtaV9GjJk0_LKHa4DamYnGuWJeh6Mw_9WZkhb51xu9Kavl3juiU63z-Cmcmv2pvqIuMaw0r8cRWhACFH9f1SB9bcW0du-HO4I85m9bsu47MCkYp1gSgqhL8X1cknco3leTtvs=792DFF48"
# os.environ["JIRA_PROJECTS_FILTER"] = "AIAG"
# mcp_session.DEFAULT_TIMEOUT = 60
#
#
# async def main():
#     openai_model_client = OpenAIChatCompletionClient(model="gpt-4o-mini",
#                                                      api_key="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")
#
#
#     jira_server = StdioServerParams(command = "docker", args= ["run",
#         "-i",
#         "--rm",
#         "--dns" , "8.8.8.8" , "--dns","1.1.1.1",
#         "-e", f"JIRA_URL={os.environ['JIRA_URL']}",
#         "-e", f"JIRA_USERNAME={os.environ['JIRA_USERNAME']}",
#         "-e", f"JIRA_API_TOKEN={os.environ['JIRA_API_TOKEN']}",
#          "-e", f"JIRA_PROJECTS_FILTER={os.environ['JIRA_PROJECTS_FILTER']}",
#         "ghcr.io/sooperset/mcp-atlassian:latest"])
#     jira_workbench = McpWorkbench(jira_server)
#
#     file_server = StdioServerParams(command = "npx" , args = ["-y",
#         "@modelcontextprotocol/server-filesystem",
#         "C:/Users/T2002135/PycharmProjects/AgenticAI"] , read_timeout_seconds=120)
#     file_workbench = McpWorkbench(file_server)
#
#     playwright_server = StdioServerParams(command = "npx" , args = ["@playwright/mcp@latest"], read_timeout_seconds=60)
#     playwright_workbench = McpWorkbench(playwright_server)
#
#     async with jira_workbench as jira_instance, file_workbench as file_instance, playwright_workbench as playwright_instance:
#
#         jira_assistance = AssistantAgent(name="JiraAgent", model_client=openai_model_client, workbench=jira_instance ,
#                                       system_message="You are a Jira Test Analyst specializing in deriving the test scenarios from Jira User stories."
#                                              "You are connected to Jira via MCP. If Jira data is not available, do NOT create hypothetical user stories."
#                                             "Instead, report the error clearly: Jira data could not be retrieved."
#                                             "Your task is as follows:"
#                                             "Goal - - Your role is to analyze user stories and create comprehensive test scenarios."
#                                             "1. Retrieve and review the most recent User story or the last created user story from the 'AIAG Project' (Project Key: `AIAG`) in Jira."
#                                             "2. Carefully read their descriptions and Acceptance criteria and identify 'requirements or common patterns'"
#                                             "3. Based on these patterns, design a 'detailed user flow' that exercises the core features of the application and can serve as a robust 'smoke test scenario'."
#
#                                             "Be very specific in your smoke test design:"
#                                             "-Provide clear, step-by-step manual testing instructions."
#                                             "- Include exact 'URLs or page routes' to visit."
#                                             "- Describe 'user actions' (clicks, form inputs, submissions,Enter text etc)."
#                                             "- Clearly state the 'expected outcomes or validations' for each step."
#
#
#                                             "When your analysis and scenario preparation is complete:"
#                                             "- Clearly output the final smoke testing steps."
#                                             "- Finally, write: 'Pass to Automation' to signal completion of your analysis.")
#
#         file_assistance = AssistantAgent(name="FileAgent", model_client=openai_model_client, workbench=file_instance,
#                                         system_message="you are a File management expert. Your task is to write the test scenarios created by the Jira assistant to a file in the local filesystem with clear test steps and with generated test case id as user story id for better traceability."
#                                                        "test steps should properly formatted with clear instructions and expected results.")
#
#         automation_assistance = AssistantAgent(name="AutomationAgent", model_client=openai_model_client, workbench=playwright_instance,
#                                         system_message= "You are a Playwright automation expert. Take the user flow from jira or file assistance and convert it into "
#             "executable Playwright commands. Use Playwright MCP tools to execute the smoke test. "
#                                                         "Handle dialogs only if a modal is present."
#                 "Ignore non-critical resource failures (404/403) and continue execution.Execute the "
#             "automated test step by step and report results clearly and wait for the page to load and images are loaded, including any errors or successes. Take screenshots "
#             "at key points to document the test execution. Make sure expected results in the test scenarios are validated "
#             "in your flow. Important: Use browser_wait_for to wait for success/error messages, wait for buttons to change "
#             "state (e.g., 'Applying...' to complete), verify expected outcomes as specified by file assistance. Always "
#             "follow the exact timing and waiting instructions provided. Complete ALL steps before saying 'TESTING COMPLETE'")
#
#         terminate_conditions = TextMentionTermination("TESTING COMPLETE") | TextMentionTermination("Jira data could not be retrieved") | TextMentionTermination("Failed to load resource: the server responded with a status of 404")
#
#         group = RoundRobinGroupChat(participants=[jira_assistance,file_assistance, automation_assistance],termination_condition=terminate_conditions)
#
#         await Console(group.run_stream(task="Jira assistance :"
#                                             "1. Search the last created user story from the project AIAG"
#                                             "2. Design a stable user scenarios for stable smoke tests"
#                                             "3. Launch the base url as 'https://condor:C7gyVWN3@www-stage.condor.com/tca/eu/flight/search'"
#                                             "file assistance :cleary write the test scenarios created by the Jira assistance to a file in the local filesystem with clear test steps and with generated test case id as user story id for better traceability."
#                                             "Automation assistance :"
#                                             "Once the test scenario creation completed,automate the user test scenarios using playwright mcp tool headed mode which created by jira assistant"))
#         await openai_model_client.close()
#
#
# asyncio.run(main())
from autogen_ext.tools.mcp import StdioServerParams, McpWorkbench
import os

import mcp.shared.session as mcp_session

class MCPInstance:

    os.environ["JIRA_URL"] = "https://viveksvvek.atlassian.net"
    os.environ["JIRA_USERNAME"] = "viveksvvek@gmail.com"
    os.environ[
        "JIRA_API_TOKEN"] = "ATATT3xFfGF0vxwF2O98p5lIEXSuZw4Oa4oKcfrA_aRbvaMM-dzTctz6thihQ6A45HOa9h6J1_M7u_VHmE16P26fE-mxMbp_HSDrrhBR_68pZ-xJWa77oRnmQ2YFFbMi8NIEOcqDAEiuACed-_sbE0y2WZneTOyYQZBO0e9ztdnMrg9YTEz60F4=A323121F"
    os.environ["JIRA_PROJECTS_FILTER"] = "AIAG"
    mcp_session.DEFAULT_TIMEOUT = 120

    @staticmethod
    def get_jira_instance():
        jira_server = StdioServerParams(command="docker", args=["run",
                                                                "-i",
                                                                "--rm",
                                                                "--dns", "8.8.8.8", "--dns", "1.1.1.1",
                                                                "-e", f"JIRA_URL={os.environ['JIRA_URL']}",
                                                                "-e", f"JIRA_USERNAME={os.environ['JIRA_USERNAME']}",
                                                                "-e", f"JIRA_API_TOKEN={os.environ['JIRA_API_TOKEN']}",
                                                                "-e",
                                                                f"JIRA_PROJECTS_FILTER={os.environ['JIRA_PROJECTS_FILTER']}",
                                                                "ghcr.io/sooperset/mcp-atlassian:latest"], read_timeout_seconds=120)
        return McpWorkbench(jira_server)

    @staticmethod
    def get_file_instance():
        file_server = StdioServerParams(command="npx", args=["-y",
                                                            "@modelcontextprotocol/server-filesystem",
                                                            "C:\\Users\\T2002135\\PycharmProjects\\AgenticAI",
                                                             "C:\\Users\\T2002135\\"], read_timeout_seconds=120)
        return McpWorkbench(file_server)

    @staticmethod
    def get_playwright_instance():
        playwright_server = StdioServerParams(command="npx", args=["@playwright/mcp@latest"],
                                             read_timeout_seconds=60)
        return McpWorkbench(playwright_server)

    @staticmethod
    def get_selenium_instance():
        selenium_server = StdioServerParams(command="npx", args=["-y","@angiejones/mcp-selenium"],
                                             read_timeout_seconds=60)
        return McpWorkbench(selenium_server)

    @staticmethod
    def get_report_instance():
        report_server = StdioServerParams(command="npx", args=["-y", "@klavis-ai/report_generation-mcp-server@latest"],
                                            read_timeout_seconds=60)
        return McpWorkbench(report_server)
from configparser import ConfigParser


class Base:

    def __init__(self):
        self.config = ConfigParser()
        self.config.read("config.ini")

    def get_model_client(self):
        return self.config.get('DEFAULT', 'model_client')


    def get_api_key(self):
       return self.config.get('DEFAULT', 'api_key')

    def get_jira_context(self):
        return self.config.get('SYSTEM_MESSAGES', 'jira_context')

    def get_file_context(self):
        return self.config.get('SYSTEM_MESSAGES', 'file_context')

    def get_automation_context(self):
        return self.config.get('SYSTEM_MESSAGES', 'automation_context')
from autogen_agentchat.conditions import TextMentionTermination


class Terminate:

    @staticmethod
    def get_text_mention_termination():
        return TextMentionTermination("TESTING COMPLETE") | TextMentionTermination(
            "Jira data could not be retrieved") | TextMentionTermination(
            "Failed to load resource: the server responded with a status of 404")

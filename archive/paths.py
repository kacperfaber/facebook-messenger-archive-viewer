class PathProvider:
    def __init__(self, working_dir):
        self.working_dir = working_dir

    def get_messages(self):
        """
        :return: /messages folder
        """
        return f"{self.working_dir}/messages"

    def get_archived_threads(self):
        """
        :return: archived threads folder
        """
        return f"{self.working_dir}/messages/archived_threads"

    def get_inbox(self):
        """
        :return: inbox folder
        """
        return f"{self.working_dir}/messages/inbox"

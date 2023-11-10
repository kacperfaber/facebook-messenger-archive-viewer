from os.path import join


class PathProvider:
    def __init__(self, working_dir):
        self.working_dir = working_dir

    def get_messages(self):
        """
        :return: /messages folder
        """
        return join(self.working_dir, "messages")

    def get_archived_threads(self):
        """
        :return: archived threads folder
        """
        return join(self.working_dir, "messages", "archived_threads")

    def get_inbox(self):
        """
        :return: inbox folder
        """
        return join(self.working_dir, "messages", "inbox")

    def get_message_requests(self):
        """
        :return: message_requests directory
        """
        return join(self.working_dir, "messages", "message_requests")

    def get_filtered_threads(self):
        """
        :return: filtered_threads directory
        """
        return join(self.working_dir, "messages", "filtered_threads")

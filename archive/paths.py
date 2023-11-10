from os.path import join


# noinspection PyMethodMayBeStatic
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

    def get_photos(self, conversation_dir_abs) -> str:
        """
        :param conversation_dir_abs: Absolute path of the directory for example: '.../messages/lipiecgril_0303''
        :return: Photos directory absolute path
        """
        return join(conversation_dir_abs, "photos")

    def get_videos(self, conversation_dir_abs) -> str:
        """
        :param conversation_dir_abs: Absolute path of the directory for example: 'fb/messages/inbox/lipiecgril_0303''
        :return: Videos directory absolute path
        """
        return join(conversation_dir_abs, "videos")

    def get_gifs(self, conversation_dir_abs) -> str:
        """
        :param conversation_dir_abs: Absolute path of the directory for example: 'fb/messages/inbox/lipiecgril_0303''
        :return: Gifs directory absolute path
        """
        return join(conversation_dir_abs, "gifs")

    def get_audio(self, conversation_dir_abs) -> str:
        """
        :param conversation_dir_abs: Absolute path of the directory for example: 'fb/messages/inbox/lipiecgril_0303''
        :return: Audio directory absolute path
        """
        return join(conversation_dir_abs, "audio")
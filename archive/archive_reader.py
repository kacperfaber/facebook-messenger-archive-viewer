import json
import os

from archive.conversation_reader import ConversationReader
from archive.models import *
from archive.paths import PathProvider
from typing import List
from os.path import join


class ArchiveReader:
    def __init__(self, working_dir):
        self.path_provider = PathProvider(working_dir)

    # noinspection PyMethodMayBeStatic
    def __read_conversations_from_directory(self, directory) -> List[BigConversation]:
        return [ConversationReader(conversation_dir=join(directory, c_dir), path_provider=self.path_provider).read_conversation() for c_dir in os.listdir(directory)]

    def read_archive(self) -> Archive:
        archive = Archive()
        archive.archived_threads = self.__read_conversations_from_directory(self.path_provider.get_archived_threads())
        archive.inbox = self.__read_conversations_from_directory(self.path_provider.get_inbox())
        archive.message_requests = self.__read_conversations_from_directory(self.path_provider.get_message_requests())
        archive.filtered_threads = self.__read_conversations_from_directory(self.path_provider.get_filtered_threads())
        return archive

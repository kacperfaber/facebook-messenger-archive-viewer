from archive.models import Conversation, BigConversation, Message
import os
from typing import List
import jsons


class ConversationReader:
    def __init__(self, conversation_dir):
        self.conversation_dir = conversation_dir

    def __get_all_conversation_files(self):
        return [os.path.join(self.conversation_dir, file) for file in os.listdir(self.conversation_dir) if
                file.endswith(".json")
                and file.startswith("message")
                and os.path.isfile(os.path.join(self.conversation_dir, file))]

    # noinspection PyMethodMayBeStatic
    def __create_conversations_of_files(self, json_files) -> List[Conversation]:
        ret: List[Conversation] = []
        for json_file in json_files:
            with open(json_file) as file:
                file_content = file.read()
                ret.append(jsons.loads(file_content, Conversation))
        return ret

    # noinspection PyMethodMayBeStatic
    def __join_messages(self, conversations: List[Conversation]) -> List[Message]:
        messages: List[Message] = []
        for c in conversations:
            messages.extend(c.messages)
        return messages

    def __create_big_conversation(self, conversations: List[Conversation]) -> BigConversation | None:
        if len(conversations) > 0:
            c = conversations[0]
            return BigConversation(title=c.title,
                                   is_still_participant=c.is_still_participant,
                                   thread_type=c.thread_type,
                                   thread_path=c.thread_path,
                                   messages=self.__join_messages(conversations))
        else:
            return None

    def read_conversation(self) -> BigConversation | None:
        message_files = self.__get_all_conversation_files()
        conversations: List[Conversation] = self.__create_conversations_of_files(message_files)
        return self.__create_big_conversation(conversations)

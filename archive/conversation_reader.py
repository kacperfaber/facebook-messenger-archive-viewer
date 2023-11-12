from archive.models import Conversation, BigConversation, Message
import os
from typing import List
import jsons

from archive.paths import PathProvider


class ConversationReader:
    def __init__(self, conversation_dir: str, path_provider: PathProvider):
        self.conversation_dir = conversation_dir
        self.path_provider = path_provider

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

    def __listdir_relative_to_working_dir_paths(self, dir1: str):
        x = [os.path.relpath(os.path.join(dir1, d), self.path_provider.working_dir) for d in os.listdir(dir1) if os.path.isfile(os.path.join(dir1, d))]
        return x

    # noinspection PyMethodMayBeStatic
    def __listdir_absolute_paths(self, dir1: str):
        return [os.path.join(dir1, d) for d in os.listdir(dir1)]

    # noinspection PyMethodMayBeStatic
    def __join_messages(self, conversations: List[Conversation]) -> List[Message]:
        messages: List[Message] = []
        for c in conversations:
            messages.extend(c.messages)
        return messages

    def __get_videos(self) -> List[str]:
        video_path = self.path_provider.get_videos(conversation_dir_abs=self.conversation_dir)
        if os.path.exists(video_path):
            return self.__listdir_relative_to_working_dir_paths(video_path)
        else:
            return []

    def __get_photos(self) -> List[str]:
        photo_path = self.path_provider.get_photos(self.conversation_dir)
        if os.path.exists(photo_path):
            return self.__listdir_relative_to_working_dir_paths(photo_path)
        else:
            return []

    def __get_gifs(self) -> List[str]:
        gif_path = self.path_provider.get_gifs(self.conversation_dir)
        if os.path.exists(gif_path):
            return self.__listdir_relative_to_working_dir_paths(gif_path)
        else:
            return []

    def __get_audio(self) -> List[str]:
        audio_path = self.path_provider.get_audio(self.conversation_dir)
        if os.path.exists(audio_path):
            return self.__listdir_relative_to_working_dir_paths(audio_path)
        else:
            return []

    def __get_conversation_relative_path(self) -> str:
        return os.path.relpath(self.conversation_dir, self.path_provider.working_dir)

    def __create_big_conversation(self, conversations: List[Conversation]) -> BigConversation | None:
        if len(conversations) > 0:
            c = conversations[0]
            return BigConversation(title=c.title,
                                   is_still_participant=c.is_still_participant,
                                   thread_type=c.thread_type,
                                   thread_path=c.thread_path,
                                   messages=self.__join_messages(conversations),
                                   audio=self.__get_audio(),
                                   videos=self.__get_videos(),
                                   photos=self.__get_photos(),
                                   gifs=self.__get_gifs(),
                                   rel_path=self.__get_conversation_relative_path())
        else:
            return None

    def read_conversation(self) -> BigConversation | None:
        if not os.path.exists(self.conversation_dir):
            return None

        message_files = self.__get_all_conversation_files()
        conversations: List[Conversation] = self.__create_conversations_of_files(message_files)
        return self.__create_big_conversation(conversations)

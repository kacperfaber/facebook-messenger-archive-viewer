from typing import List
from sqlalchemy import create_engine

from archive.archive_reader import ArchiveReader
from archive.models import BigConversation
from image.converters import Converters
from image.data_reader import DataReader
from image.db import Db
from image.dtos import ThreadLocation, ThreadDto
from archive.paths import join_rel_path


# noinspection PyMethodMayBeStatic
class ImageBuilder:
    def __init__(self, engine):
        self.data_reader = DataReader()
        self.db = Db(engine=engine)

    def build_image(self, archive_dir: str) -> None:
        archive = ArchiveReader(working_dir=archive_dir).read_archive()

        k = [
            {"loc": ThreadLocation.INBOX, "data": archive.inbox},
            {"loc": ThreadLocation.FILTERED_THREADS, "data": archive.filtered_threads},
            {"loc": ThreadLocation.ARCHIVED, "data": archive.archived_threads},
            {"loc": ThreadLocation.MESSAGE_REQUESTS, "data": archive.message_requests},
        ]

        for item in k:
            self.__save_threads_as(working_dir=archive_dir, conversations=item["data"], thread_location=item["loc"])

    def __create_all_attachments(self, conversation: BigConversation, working_dir: str) -> int:
        for photo_rel_path in conversation.photos:
            photo_absolute = join_rel_path(working_dir=working_dir, rel_path=photo_rel_path)
            self.db.save_photo_attachment(photo_rel_path, self.data_reader.read_data_as_base64(photo_absolute))

        for video_rel_path in conversation.videos:
            video_absolute = join_rel_path(working_dir=working_dir, rel_path=video_rel_path)
            data = self.data_reader.read_data_as_base64(video_absolute)
            self.db.save_video_attachment(rel_path=video_rel_path, data=data)

        for gif_rel_path in conversation.gifs:
            gif_abs = join_rel_path(working_dir=working_dir, rel_path=gif_rel_path)
            data = self.data_reader.read_data_as_base64(gif_abs)
            self.db.save_gif_attachment(rel_path=gif_rel_path, data=data)

        for audio_rel_path in conversation.audio:
            audio_abs = join_rel_path(working_dir=working_dir, rel_path=audio_rel_path)
            data = self.data_reader.read_data_as_base64(audio_abs)
            self.db.save_audio_attachment(rel_path=audio_rel_path, data=data)

        return len(conversation.photos) + len(conversation.audio) + len(conversation.videos) + len(conversation.gifs)

    def __create_thread(self, conversation: BigConversation, thread_location: ThreadLocation) -> ThreadDto:
        thread_dto = Converters.big_conversation_to_thread(c=conversation, thread_location=thread_location)
        thread_dto.messages = [Converters.message_to_message_dto(msg) for msg in conversation.messages]
        return thread_dto

    def __save_threads_as(self, working_dir: str, conversations: List[BigConversation],
                          thread_location: ThreadLocation):
        for conversation in conversations:
            self.__create_all_attachments(conversation, working_dir=working_dir)
            self.db.save_thread(self.__create_thread(conversation, thread_location))


def create_image_builder(image_name: str, password: str | None = None, echo: bool = False) -> ImageBuilder:
    engine = Db.create_engine(image_name=image_name, password=password, echo=echo)
    return ImageBuilder(engine=engine)

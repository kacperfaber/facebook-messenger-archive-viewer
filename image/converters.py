import datetime

from archive.models import Message, Photo, Video, Audio
from image.dtos import MessageDto, MessageType, MessageAttachmentDto, MessageAttachmentType


class Converters:

    @staticmethod
    def timestamp_ms_to_datetime(timestamp_ms: int) -> datetime.datetime:
        return datetime.datetime.fromtimestamp(timestamp_ms / 1000)

    @staticmethod
    def timestamp_to_datetime(timestamp: int) -> datetime.datetime:
        return datetime.datetime.fromtimestamp(timestamp)

    # noinspection PyPep8Naming
    @staticmethod
    def message_type_to_MessageType(type1: str) -> MessageType:
        if type1 == 'Generic':
            return MessageType.GENERIC

        elif type1 == 'Call':
            return MessageType.CALL

        raise Exception(f"Unknown message type '{type1}'")

    @staticmethod
    def convert_attachment(attachment: Photo | Video | Audio) -> MessageAttachmentDto:
        if isinstance(attachment, Photo):
            return MessageAttachmentDto(uri=attachment.uri,
                                        type1=MessageAttachmentType.PHOTO,
                                        created_at=Converters.timestamp_to_datetime(attachment.creation_timestamp))

        elif isinstance(attachment, Video):
            return MessageAttachmentDto(attachment.uri, type1=MessageAttachmentType.VIDEO,
                                        thumbnail_uri=attachment.thumbnail.uri,
                                        created_at=Converters.timestamp_to_datetime(attachment.creation_timestamp))

        elif isinstance(attachment, Audio):
            return MessageAttachmentDto(attachment.uri, type1=MessageAttachmentType.AUDIO)

        raise Exception(f'Unknown attachment type "{type(attachment)}". Possible: Photo, Video, Audio.')

    @staticmethod
    def __apply_attachments(message: Message, message_dto: MessageDto):
        x = [Converters.convert_attachment(a) for a in [*message.photos, *message.videos, *message.audio_files]]
        message_dto.attachments = x

    @staticmethod
    def message_to_message_dto(message: Message) -> MessageDto:
        m = MessageDto()
        m.content = message.content
        m.sender_name = message.sender_name
        m.sent_at = Converters.timestamp_ms_to_datetime(message.timestamp_ms)
        m.type = Converters.message_type_to_MessageType(message.type)

        if m.type == MessageType.CALL:
            m.call_duration = message.call_duration

        Converters.__apply_attachments(message, m)

        return m

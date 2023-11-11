import datetime

from archive.models import Message, Photo, Video, Audio, BigConversation
from image.dtos import MessageDto, MessageType, MessageAttachmentDto, MessageAttachmentType, ThreadDto, ThreadType, \
    ThreadLocation


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

        elif type1 == "Share":
            return MessageType.SHARE

        elif type1 == "Subscribe":
            return MessageType.SUBCRIBE

        elif type1 == "Unsubscribe":
            return MessageType.UNSUBCRIBE

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
        x = [Converters.convert_attachment(a) for a in [*getattr(message, "photos", []), *getattr(message, "videos", []), *getattr(message, "audio_files", [])]]
        message_dto.attachments = x

    @staticmethod
    def message_to_message_dto(message: Message) -> MessageDto:
        m = MessageDto()
        m.content = getattr(message, "content", None)
        m.sender_name = message.sender_name
        m.sent_at = Converters.timestamp_ms_to_datetime(message.timestamp_ms)
        m.type = Converters.message_type_to_MessageType(message.type)

        if m.type == MessageType.CALL:
            m.call_duration = message.call_duration

        Converters.__apply_attachments(message, m)

        return m

    @staticmethod
    def convert_thread_type(thread_type: str) -> ThreadType:
        if thread_type == 'RegularGroup':
            return ThreadType.GROUP
        elif thread_type == 'Regular':
            return ThreadType.CONVERSATION
        elif thread_type == "Pending":
            return ThreadType.PENDING
        raise Exception(f"Unknown thread_type '{thread_type}'")

    @staticmethod
    def big_conversation_to_thread(c: BigConversation, thread_location: ThreadLocation) -> ThreadDto:
        thread_type = Converters.convert_thread_type(c.thread_type)
        return ThreadDto(title=c.title, thread_type=thread_type, thread_path=c.thread_path,
                         thread_location=thread_location, rel_path=c.rel_path)

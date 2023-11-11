import datetime
from enum import Enum as PythonEnum

from sqlalchemy import Column, String, Enum, Integer, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

DeclarativeDb = declarative_base()


class ThreadType(PythonEnum):
    GROUP = 'group'
    CONVERSATION = 'conversation'


class ThreadLocation(PythonEnum):
    ARCHIVED = 'archived'
    INBOX = 'inbox'
    MESSAGE_REQUESTS = 'message_requests'
    FILTERED_THREADS = 'filtered_threads'


# noinspection SpellCheckingInspection
class ThreadDto(DeclarativeDb):
    __tablename__ = "threads"

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String, nullable=False)
    thread_type = Column(Enum(ThreadType), nullable=False)
    thread_path = Column(String, nullable=False)
    location = Column(Enum(ThreadLocation), nullable=False)
    messages = relationship("MessageDto")

    def __init__(self, title: str, thread_type: ThreadType, thread_path: str):
        self.title = title
        self.thread_type = thread_type
        self.thread_path = thread_path


class MessageType(PythonEnum):
    CALL = 'call'
    GENERIC = 'generic'


# noinspection SpellCheckingInspection
class MessageDto(DeclarativeDb):
    __tablename__ = "messages"
    id = Column(Integer, primary_key=True, autoincrement=True)

    # Relation with Thread
    thread_id = Column(Integer, ForeignKey("threads.id"))
    thread = relationship("ThreadDto", back_populates="messages")

    sender_name = Column(String, nullable=False)
    sent_at = Column(DateTime, nullable=False)
    content = Column(String, nullable=False)
    type = Column(Enum(MessageType), nullable=False)
    call_duration = Column(Integer, nullable=True)
    attachments = relationship("MessageAttachmentDto", back_populates="message")


class AttachmentType(PythonEnum):
    PHOTO = 'photo'
    VIDEO = 'video'
    GIF = 'gif'
    AUDIO = 'audio'


# noinspection SpellCheckingInspection
class AttachmentDto(DeclarativeDb):
    __tablename__ = "attachments"
    id = Column(Integer, primary_key=True, autoincrement=True)
    type = Column(Enum(AttachmentType), nullable=False)
    data = Column(String, nullable=False)
    path = Column(String, nullable=False)

    def __init__(self, type1: AttachmentType, data: str, path: str):
        self.type = type1
        self.data = data
        self.path = path


class MessageAttachmentType(PythonEnum):
    PHOTO = 'photo'
    VIDEO = 'video'
    GIF = 'gif'
    AUDIO = 'audio'


# noinspection SpellCheckingInspection
class MessageAttachmentDto(DeclarativeDb):
    __tablename__ = "message_attachments"
    id = Column(Integer, primary_key=True, autoincrement=True)
    message_id = Column(Integer, ForeignKey("messages.id"))
    message = relationship("MessageDto", back_populates="attachments")
    uri = Column(String, nullable=False)
    type = Column(Enum(MessageAttachmentType), nullable=False)

    def __init__(self, uri: str):
        self.uri = uri

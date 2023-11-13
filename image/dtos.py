import dataclasses
import datetime
from enum import Enum as PythonEnum
from typing import List

from sqlalchemy import Column, String, Enum, Integer, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, Mapped

DeclarativeDb = declarative_base()


class ThreadType(str, PythonEnum):
    GROUP = 'group'
    CONVERSATION = 'conversation'
    PENDING = 'pending'  # Generally in message_requests


class ThreadLocation(str, PythonEnum):
    ARCHIVED = 'archived'
    INBOX = 'inbox'
    MESSAGE_REQUESTS = 'message_requests'
    FILTERED_THREADS = 'filtered_threads'


class MessageType(str, PythonEnum):
    SHARE = "share"  # "username sent a live location"
    CALL = 'call'
    GENERIC = 'generic'
    SUBCRIBE = 'subscribe'  # "username1 added username2 to the group."
    UNSUBCRIBE = 'unsubscribe'  # "You left the group." / "username1 left the group"


class MessageAttachmentType(str, PythonEnum):
    PHOTO = 'photo'
    VIDEO = 'video'
    GIF = 'gif'
    AUDIO = 'audio'


# noinspection SpellCheckingInspection
@dataclasses.dataclass
class MessageAttachmentDto(DeclarativeDb):
    __tablename__ = "message_attachments"
    id: int = Column(Integer, primary_key=True, autoincrement=True)
    message_id: int = Column(Integer, ForeignKey("messages.id"))
    message = relationship("MessageDto", back_populates="attachments")
    uri: str = Column(String, nullable=False)
    thumbnail_uri: str = Column(String, nullable=True)
    created_at: datetime.datetime = Column(DateTime, nullable=True)
    type: MessageAttachmentType = Column(Enum(MessageAttachmentType), nullable=False)

    def __init__(self, uri: str, type1: MessageAttachmentType, thumbnail_uri: str | None = None,
                 created_at: datetime.datetime | None = None):
        self.uri = uri
        self.thumbnail_uri = thumbnail_uri
        self.created_at = created_at
        self.type = type1


# noinspection SpellCheckingInspection
@dataclasses.dataclass
class MessageDto(DeclarativeDb):
    __tablename__ = "messages"
    id: int = Column(Integer, primary_key=True, autoincrement=True)

    # Relation with Thread
    thread_id: int = Column(Integer, ForeignKey("threads.id"))
    thread = relationship("ThreadDto", back_populates="messages")

    sender_name: str = Column(String, nullable=False)
    sent_at: datetime.datetime = Column(DateTime, nullable=False)
    content: str = Column(String, nullable=True)
    type: MessageType = Column(Enum(MessageType), nullable=False)
    call_duration: int = Column(Integer, nullable=True)
    attachments: Mapped[List[MessageAttachmentDto]] = relationship("MessageAttachmentDto", back_populates="message")


class AttachmentType(str, PythonEnum):
    PHOTO = 'photo'
    VIDEO: str = 'video'
    GIF: str = 'gif'
    AUDIO: str = 'audio'


# noinspection SpellCheckingInspection
@dataclasses.dataclass
class AttachmentDto(DeclarativeDb):
    __tablename__ = "attachments"
    id: int = Column(Integer, primary_key=True, autoincrement=True)
    type: AttachmentType = Column(Enum(AttachmentType), nullable=False)
    data: str = Column(String, nullable=False)
    path: str = Column(String, nullable=False)

    def __init__(self, type1: AttachmentType, data: str, path: str):
        self.type = type1
        self.data = data
        self.path = path


# noinspection SpellCheckingInspection
@dataclasses.dataclass
class ThreadDto(DeclarativeDb):
    __tablename__ = "threads"

    id: int = Column(Integer, primary_key=True, autoincrement=True)
    title: str = Column(String, nullable=False)
    thread_type: str = Column(Enum(ThreadType), nullable=False)
    thread_path: str = Column(String, nullable=False)
    rel_path: str = Column(String, nullable=False)
    location: str = Column(Enum(ThreadLocation), nullable=False)
    messages = relationship("MessageDto")

    def __init__(self, title: str, thread_type: ThreadType, thread_path: str, thread_location: ThreadLocation,
                 rel_path: str):
        self.title = title
        self.thread_type = thread_type
        self.thread_path = thread_path
        self.location = thread_location
        self.rel_path = rel_path

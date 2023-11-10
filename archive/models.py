from typing import List


class Reaction:
    reaction: str
    actor: str  # User name


class Photo:
    uri: str  # For example: messages/inbox/our-class/photos/xd.jpg
    creation_timestamp: int


class Thumbnail:
    uri: str


class Video:
    uri: str
    creation_timestamp: int
    thumbnail: Thumbnail


class Message:
    sender_name: str
    timestamp_ms: int
    content: str
    type: str  # 'Generic' / 'Call'
    call_duration: int
    is_unsent: bool
    reactions: List[Reaction]
    photos: List[Photo]


class Participant:
    name: str


class Conversation:
    messages: List[Message]
    participants: List[Participant]
    title: str
    is_still_participant: bool
    thread_type: str  # RegularGroup / Regular
    thread_path: str


class BigConversation:
    def __init__(self, title, is_still_participant, thread_type, thread_path, messages):
        self.title = title
        self.thread_path = thread_path
        self.thread_type = thread_type
        self.is_still_participant = is_still_participant
        self.messages = messages

    title: str
    is_still_participant: bool
    thread_type: str  # RegularGroup / Regular
    thread_path: str
    messages: List[Message]


class Archive:
    archived_threads: List[Conversation]
    inbox: List[Conversation]
    filtered_threads: List[Conversation]
    message_requests: List[Conversation]

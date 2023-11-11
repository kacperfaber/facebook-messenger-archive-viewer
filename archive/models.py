from typing import List


class Reaction:
    reaction: str
    actor: str  # User name


class Photo:
    uri: str  # For example: messages/inbox/our-class/photos/xd.jpg
    creation_timestamp: int

    def __init__(self, uri, creation_timestamp):
        self.uri = uri
        self.creation_timestamp = creation_timestamp


class Thumbnail:
    uri: str

    def __init__(self, uri):
        self.uri = uri


class Video:
    uri: str
    creation_timestamp: int
    thumbnail: Thumbnail

    def __init__(self, uri: str, creation_timestamp: int, thumbnail: Thumbnail):
        self.uri = uri
        self.creation_timestamp = creation_timestamp
        self.thumbnail = thumbnail


class Audio:
    uri: str

    def __init__(self, uri: str):
        self.uri = uri


class Message:
    sender_name: str
    timestamp_ms: int
    content: str
    type: str  # 'Generic' / 'Call'
    call_duration: int
    is_unsent: bool
    reactions: List[Reaction]
    photos: List[Photo]
    videos: List[Video]
    audio_files: List[Audio]


class Participant:
    name: str


class Conversation:
    def __init__(self, messages: List[Message], participants: List[Participant], title: str, is_still_participant: bool, thread_type: str, thread_path: str):
        self.messages = messages
        self.participants = participants
        self.title = title
        self.thread_path = thread_path
        self.thread_type = thread_type
        self.is_still_participant = is_still_participant

    messages: List[Message]
    participants: List[Participant]
    title: str
    is_still_participant: bool
    thread_type: str  # RegularGroup / Regular
    thread_path: str


class BigConversation:
    def __init__(self, title, is_still_participant, thread_type, thread_path, messages, photos: List[str], videos: List[str], gifs: List[str], audio: List[str], rel_path):
        self.title = title
        self.thread_path = thread_path
        self.thread_type = thread_type
        self.is_still_participant = is_still_participant
        self.messages = messages
        self.videos = videos
        self.photos = photos
        self.gifs = gifs
        self.audio = audio
        self.rel_path = rel_path

    title: str
    rel_path: str  # Relative to working dir path to conversation directory
    is_still_participant: bool
    thread_type: str  # RegularGroup / Regular
    thread_path: str  # Relative to $working_dir/messages directory to conversation directory example: inbox/john_smith
    messages: List[Message]
    videos: List[str]  # Relative to working dir paths to all videos under conversation
    photos: List[str]  # Relative to working dir paths to all photos under conversation
    gifs: List[str]  # Relative to working dir paths to all gifs under conversation
    audio: List[str]  # Relative to working dir paths to all audio under conversation


class Archive:
    archived_threads: List[BigConversation]
    inbox: List[BigConversation]
    filtered_threads: List[BigConversation]
    message_requests: List[BigConversation]

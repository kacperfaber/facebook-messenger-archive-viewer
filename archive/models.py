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
    reactions: [Reaction]
    photos: [Photo]


class Participant:
    name: str


class Conversation:
    messages: [Message]
    participants: [Participant]
    title: str
    is_still_participant: bool
    thread_type: str  # RegularGroup / Regular
    thread_path: str

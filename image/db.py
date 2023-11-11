from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

from image.dtos import DeclarativeDb, AttachmentDto, AttachmentType


class Db:
    def __init__(self, engine):
        self.engine = engine
        DeclarativeDb.metadata.create_all(self.engine)
        self.session = sessionmaker(bind=self.engine)
        self.session = Session(bind=self.engine)

    def __save_attachment(self, type1: AttachmentType, rel_path: str, data: str) -> AttachmentDto:
        attachment = AttachmentDto(type1=type1, data=data, path=rel_path)
        self.session.add(attachment)
        self.session.commit()
        return attachment

    def save_photo_attachment(self, rel_path: str, data: str) -> int:
        attachment = AttachmentDto(AttachmentType.PHOTO, data, rel_path)
        self.session.add(attachment)
        self.session.commit()
        return attachment.id

    def get_attachment_by_id(self, id1: int) -> AttachmentDto | None:
        return self.session.query(AttachmentDto).filter_by(id=id1).first()

    def save_video_attachment(self, rel_path: str, data: str) -> AttachmentDto:
        return self.__save_attachment(AttachmentType.VIDEO, rel_path, data)

    def save_gif_attachment(self, rel_path: str, data: str) -> AttachmentDto:
        return self.__save_attachment(AttachmentType.GIF, rel_path, data)

    def save_audio_attachment(self, rel_path: str, data: str) -> AttachmentDto:
        return self.__save_attachment(AttachmentType.AUDIO, rel_path, data)


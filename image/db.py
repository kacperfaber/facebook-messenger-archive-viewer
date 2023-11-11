from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

from image.dtos import DeclarativeDb, AttachmentDto, AttachmentType


class Db:
    def __init__(self, engine):
        self.engine = engine
        DeclarativeDb.metadata.create_all(self.engine)
        self.session = sessionmaker(bind=self.engine)
        self.session = Session(bind=self.engine)

    def save_photo_attachment(self, rel_path: str, data: str) -> int:
        attachment = AttachmentDto(AttachmentType.PHOTO, data, rel_path)
        self.session.add(attachment)
        self.session.commit()
        return attachment.id

    def get_attachment_by_id(self, id1: int) -> AttachmentDto | None:
        return self.session.query(AttachmentDto).filter_by(id=id1).first()

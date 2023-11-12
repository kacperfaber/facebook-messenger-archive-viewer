import dataclasses
from typing import Callable, List

from sqlalchemy.orm import sessionmaker, Session, Query
from sqlalchemy.engine import create_engine as alchemy_create_engine

from image.dtos import DeclarativeDb, AttachmentDto, AttachmentType, ThreadDto


@dataclasses.dataclass
class Pagination:
    items: List
    per_page: int
    page: int
    total: int

    def __init__(self, items, per_page, page, total):
        self.items = items
        self.per_page = per_page
        self.page = page
        self.total = total


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

    def save_thread(self, thread: ThreadDto):
        self.session.add(thread)
        self.session.commit()

    def q(self, entity) -> Query:
        """
        Execute query
        :return: sqlalchemy.Query
        """
        return self.session.query(entity)

    def q_paginated(self, entity, per_page: int = 10, page: int = 0):
        return self.session.query(entity).limit(per_page).offset((page - 1) * per_page)

    def pagination(self, entity, per_page: int = 10, page: int = 0, additional_steps: Callable[[Query], Query] = None):
        q = self.session.query(entity)
        q1 = q
        if additional_steps is not None:
            q1 = additional_steps(q)
        total = q1.count()
        q1 = q1.limit(per_page).offset(page * per_page)
        return Pagination(items=q1.all(), per_page=per_page, page=page, total=total)

    @staticmethod
    def create_engine(image_name: str, password: str | None, echo: bool = False):
        if password is not None:
            return alchemy_create_engine(f"sqlite+pysqlcipher://:{password}@/{image_name}.db", echo=echo)
        return alchemy_create_engine(f"sqlite:///{image_name}.sqlite", echo=echo)

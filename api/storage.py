from image.db import Db


class Storage:
    __db_key = "DB"
    __storage_dict = dict()

    @staticmethod
    def set_db(db: Db):
        Storage.__storage_dict[Storage.__db_key] = db

    @staticmethod
    def get_db() -> Db:
        return Storage.__storage_dict[Storage.__db_key]

import unittest

from sqlalchemy import create_engine

from image.db import Db
from image.dtos import AttachmentType


class DbIntegrationTest(unittest.TestCase):

    def test_save_photo_attachment_does_not_throw(self):
        engine = create_engine("sqlite://")
        db = Db(engine=engine)
        db.save_photo_attachment("/messages/image.jpg", "HelloWorld123")
        self.assertEqual(True, True)

    def test_save_photo_attachment_returns_id_is_not_None(self):
        engine = create_engine("sqlite://")
        db = Db(engine=engine)
        r = db.save_photo_attachment("", "")
        self.assertIsNotNone(r)

    def test_save_photo_attachment_returns_another_id_each_time(self):
        engine = create_engine("sqlite://")
        db = Db(engine=engine)
        r1 = db.save_photo_attachment("", "")
        r2 = db.save_photo_attachment("", "")
        self.assertNotEquals(r1, r2)

    def test_save_photo_attachment_saves_attachment_in_db(self):
        engine = create_engine("sqlite://")
        db = Db(engine=engine)
        a_id = db.save_photo_attachment("rel_path", "{}")
        get_a = db.get_attachment_by_id(id1=a_id)
        self.assertIsNotNone(get_a)

    def test_save_photo_attachment_saves_attachment_in_db_with_expected_content(self):
        engine = create_engine("sqlite://")
        db = Db(engine=engine)
        rel_path = "rel_path"
        data = "{}"
        a_id = db.save_photo_attachment(rel_path, data)
        get_a = db.get_attachment_by_id(id1=a_id)
        self.assertEqual(rel_path, get_a.path)
        self.assertEqual(data, get_a.data)

    def test_save_photo_attachment_saves_attachment_in_db_with_expected_attachment_type_eq_to_AttachmentType_PHOTO(self):
        engine = create_engine("sqlite://")
        db = Db(engine=engine)
        rel_path = "rel_path"
        data = "{}"
        a_id = db.save_photo_attachment(rel_path, data)
        get_a = db.get_attachment_by_id(id1=a_id)
        self.assertEqual(AttachmentType.PHOTO, get_a.type)

    def test_get_attachment_by_id_returns_none_if_expected(self):
        engine = create_engine("sqlite://")
        db = Db(engine=engine)
        self.assertIsNone(db.get_attachment_by_id(0))

    def test_get_attachment_by_id_returns_not_none_if_expected(self):
        engine = create_engine("sqlite://")
        db = Db(engine=engine)
        photo_attachment_id = db.save_photo_attachment("", "")
        self.assertIsNotNone(db.get_attachment_by_id(photo_attachment_id))

    def test_get_attachment_by_id_returns_expected_data(self):
        engine = create_engine("sqlite://")
        db = Db(engine=engine)
        rel_path = "rel_path"
        data = "{}"
        a_id = db.save_photo_attachment(rel_path, data)
        a = db.get_attachment_by_id(a_id)
        self.assertEqual(data, a.data)
        self.assertEqual(rel_path, a.path)
        self.assertEqual(AttachmentType.PHOTO, a.type)
        self.assertEqual(a_id, a.id)


if __name__ == '__main__':
    unittest.main()

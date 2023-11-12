import os.path
import unittest

from image.image_builder import create_image_builder


# noinspection PyMethodMayBeStatic
class ImageBuilderTest(unittest.TestCase):
    def test_create_image_builder_does_not_throw_when_using_password(self):
        create_image_builder(image_name="test", password="HelloWorld123", echo=False)

    def test_create_image_builder_does_not_throw_when_using_no_password(self):
        create_image_builder(image_name="test", echo=False)

    def test_create_image_builder_makes_sqlite_file_if_not_using_password(self):
        image_name = "001_database"
        create_image_builder(image_name=image_name, password=None)
        self.assertTrue(os.path.exists(image_name + ".sqlite"))

    def test_create_image_builder_makes_db_file_if_using_password(self):
        image_name = "002_database"
        create_image_builder(image_name=image_name, password="LikeCats")
        self.assertTrue(os.path.exists(image_name + ".db"))

    def test_create_image_builder_returns_not_none_if_using_password(self):
        self.assertIsNotNone(create_image_builder(image_name="003_database", password="LikeCats"))

    def test_create_image_builder_returns_not_none_if_not_using_password(self):
        self.assertIsNotNone(create_image_builder(image_name="003_database", password=None))

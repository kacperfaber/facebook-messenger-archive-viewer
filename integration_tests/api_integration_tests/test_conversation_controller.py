import unittest
import jsons

from api.app import App
from image.db import Pagination, Db


class ConversationControllerIntegrationTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # TODO: Need to create docker image, which will build image automatically
        db = Db(Db.create_engine(image_name="facebook_archive", password=None))
        cls.app = App(db)
        cls.app.app.config.update({"TESTING": True})
        cls.client = cls.app.app.test_client()

    def test_conversation_all_endpoint_returns_expected_200(self):
        status_code = self.client.get("/conversation/all").status_code
        self.assertEqual(200, status_code)

    # TODO: Finish tests


if __name__ == '__main__':
    unittest.main()

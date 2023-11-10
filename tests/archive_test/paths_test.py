import unittest
import platform

from archive.paths import PathProvider


@unittest.skipUnless(platform.system() == 'Linux', reason="Only for Linux")
class PathProviderLinuxTests(unittest.TestCase):
    def test_get_inbox_returns_expected_when(self):
        path_provider = PathProvider("~/Desktop/facebook")
        self.assertEqual("~/Desktop/facebook/messages/inbox", path_provider.get_inbox())

    def test_get_archived_threads_returns_expected(self):
        path_provider = PathProvider("~/Desktop/facebook")
        self.assertEqual("~/Desktop/facebook/messages/archived_threads", path_provider.get_archived_threads())

    def test_get_messages_returns_expected(self):
        path_provider = PathProvider("~/Desktop/facebook")
        self.assertEqual("~/Desktop/facebook/messages", path_provider.get_messages())

    def test_get_message_requests_returns_expected(self):
        base_path = "~/Desktop/fb"
        prov = PathProvider(base_path)
        self.assertEqual(f"{base_path}/messages/message_requests", prov.get_message_requests())

    def test_get_filtered_threads_returns_expected(self):
        base_path = "~/Desktop/fb"
        prov = PathProvider(base_path)
        self.assertEqual(f"{base_path}/messages/filtered_threads", prov.get_filtered_threads())


@unittest.skipUnless(platform.system() == 'Windows', reason="Only for Windows")
class PathProviderWindowsTests(unittest.TestCase):
    def test_get_inbox_returns_expected(self):
        path_provider = PathProvider("C:\\test_dir\\")
        self.assertEqual("C:\\test_dir\\messages\\inbox", path_provider.get_inbox())

    def test_get_archived_threads_returns_expected(self):
        path_provider = PathProvider("C:\\test_dir\\")
        self.assertEqual("C:\\test_dir\\messages\\archived_threads", path_provider.get_archived_threads())

    def test_get_messages_returns_expected(self):
        path_provider = PathProvider("C:\\test_dir\\")
        self.assertEqual("C:\\test_dir\\messages", path_provider.get_messages())

    def test_get_message_requests_returns_expected(self):
        base_path = "C:\\facebook"
        prov = PathProvider(base_path)
        self.assertEqual(f"{base_path}/messages/message_requests", prov.get_message_requests())

    def test_get_filtered_threads_returns_expected(self):
        base_path = "C:\\Users\\kacper\\fb-archive"
        prov = PathProvider(base_path)
        self.assertEqual(f"{base_path}/messages/filtered_threads", prov.get_filtered_threads())


if __name__ == '__main__':
    unittest.main()

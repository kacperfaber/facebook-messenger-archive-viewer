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


if __name__ == '__main__':
    unittest.main()

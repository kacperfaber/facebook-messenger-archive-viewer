import unittest
import platform

from archive.paths import PathProvider


@unittest.skipUnless(platform.system() == 'Linux', reason="Only for Linux")
class PathProviderLinuxTests(unittest.TestCase):
    def test_get_inbox_returns_expected_when(self):
        path_provider = PathProvider("~/Desktop/facebook")
        self.assertEqual("~/Desktop/facebook/messages/inbox", path_provider.get_inbox())


@unittest.skipUnless(platform.system() == 'Windows', reason="Only for Windows")
class PathProviderWindowsTests(unittest.TestCase):
    def test_get_inbox_returns_expected(self):
        path_provider = PathProvider("C:\\test_dir\\")
        self.assertEqual("C:\\test_dir\\messages\\inbox", path_provider.get_inbox())

    # TODO: Continue, only one method is tested


if __name__ == '__main__':
    unittest.main()

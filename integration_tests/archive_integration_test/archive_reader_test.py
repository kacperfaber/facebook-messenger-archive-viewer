import unittest

from archive.archive_reader import ArchiveReader
from integration_tests.archive_integration_test import DEFAULT_ARCHIVE_DIRECTORY


class ArchiveReaderIntegrationTest(unittest.TestCase):
    def test_read_archive_returns_not_none(self):
        res = ArchiveReader(DEFAULT_ARCHIVE_DIRECTORY).read_archive()
        self.assertIsNotNone(res)

    def test_read_archive_returns_expected_archived_threads_len(self):
        res = ArchiveReader(DEFAULT_ARCHIVE_DIRECTORY).read_archive()
        self.assertEqual(1, len(res.archived_threads))

    def test_read_archive_returns_expected_messages_len(self):
        res = ArchiveReader(DEFAULT_ARCHIVE_DIRECTORY).read_archive()
        self.assertEqual(2, len(res.archived_threads[0].messages))


if __name__ == '__main__':
    unittest.main()

import os.path
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

    def test_read_archive_returns_expected_conversation_photos_len(self):
        res = ArchiveReader(DEFAULT_ARCHIVE_DIRECTORY).read_archive()
        self.assertEqual(1, len(res.archived_threads[0].photos))

    def test_read_archive_returns_expected_conversation_photos_item(self):
        res = ArchiveReader(DEFAULT_ARCHIVE_DIRECTORY).read_archive()
        e = os.path.join(DEFAULT_ARCHIVE_DIRECTORY, "messages", "inbox", "johnsmith_37xd", "photos", "invalid_image.jpg")
        self.assertEqual(e, res.inbox[0].photos[0])

    def test_read_archive_returns_expected_conversation_videos_len(self):
        res = ArchiveReader(DEFAULT_ARCHIVE_DIRECTORY).read_archive()
        self.assertEqual(1, len(res.archived_threads[0].videos))

    def test_read_archive_returns_expected_conversation_gifs_len(self):
        res = ArchiveReader(DEFAULT_ARCHIVE_DIRECTORY).read_archive()
        self.assertEqual(1, len(res.archived_threads[0].gifs))

    def test_read_archive_returns_expected_conversation_audio_len(self):
        res = ArchiveReader(DEFAULT_ARCHIVE_DIRECTORY).read_archive()
        self.assertEqual(1, len(res.archived_threads[0].audio))

    def test_read_archive_returns_expected_rel_path(self):
        res = ArchiveReader(DEFAULT_ARCHIVE_DIRECTORY).read_archive()
        self.assertEqual("messages/inbox/johnsmith_37xd", res.inbox[0].rel_path)


if __name__ == '__main__':
    unittest.main()

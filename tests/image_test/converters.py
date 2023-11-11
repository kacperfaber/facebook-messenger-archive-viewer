import datetime
import unittest

from archive.models import Photo, Audio, Video, Thumbnail
from image.converters import Converters
from image.dtos import MessageAttachmentType, MessageType


class ConvertersTest(unittest.TestCase):
    def test_timestamp_ms_to_datetime_returns_expected_date(self):
        r = Converters.timestamp_ms_to_datetime(1622221163672)
        self.assertEqual(2021, r.year)
        self.assertEqual(28, r.day)
        self.assertEqual(5, r.month)

    def test_timestamp_ms_to_datetime_returns_expected_time(self):
        r = Converters.timestamp_ms_to_datetime(1622221163672)
        self.assertEqual(18, r.hour)
        self.assertEqual(59, r.minute)
        self.assertEqual(23, r.second)

    # noinspection PyTypeChecker
    def test_convert_attachment_throws_if_attachment_is_not_photo_video_or_audio(self):
        self.assertRaises(BaseException, Converters.convert_attachment, 5)

    def test_convert_attachment_returns_expected_if_attachment_is_photo(self):
        uri = "/test"
        creation = 1672574400
        photo_attachment = Photo(uri=uri, creation_timestamp=creation)
        r = Converters.convert_attachment(photo_attachment)
        self.assertEqual(uri, r.uri)
        self.assertEqual(datetime.datetime(2023, 1, 1, 13, 0, 0), r.created_at)

    def test_convert_attachment_returns_expected_type(self):
        self.assertEqual(first=MessageAttachmentType.AUDIO,
                         second=Converters.convert_attachment(Audio("")).type,
                         msg="Expecting MessageAttachmentType.AUDIO, when attachment is instance of Audio.")

        self.assertEqual(first=MessageAttachmentType.VIDEO,
                         second=Converters.convert_attachment(
                             Video(uri="", creation_timestamp=0, thumbnail=Thumbnail(uri=""))).type,
                         msg="Expecting MessageAttachmentType.VIDEO, when attachment is instance of Video.")

        self.assertEqual(first=MessageAttachmentType.PHOTO,
                         second=Converters.convert_attachment(Photo(uri="", creation_timestamp=0)).type,
                         msg="Expecting MessageAttachmentType.PHOTO, when attachment is instance of Photo.")

    def test_convert_attachment_returns_expected_if_attachment_is_video(self):
        uri = "/test"
        th_uri = "/tests2"
        creation = 1672574400
        video_attachment = Video(uri=uri, creation_timestamp=creation, thumbnail=Thumbnail(th_uri))
        r = Converters.convert_attachment(video_attachment)
        self.assertEqual(uri, r.uri)
        self.assertEqual(th_uri, r.thumbnail_uri)
        self.assertEqual(datetime.datetime(2023, 1, 1, 13, 0, 0), r.created_at)

    def test_convert_attachment_returns_expected_if_attachment_is_audio(self):
        uri = "/uri"
        attachment = Audio(uri)
        r = Converters.convert_attachment(attachment)
        self.assertEqual(uri, r.uri)

    def test_message_type_to_MessageType_returns_MessageType_CALL_if_expected(self):
        self.assertEqual(MessageType.CALL, Converters.message_type_to_MessageType('Call'))

    def test_message_type_to_MessageType_returns_MessageType_GENERIC_if_expected(self):
        self.assertEqual(MessageType.GENERIC, Converters.message_type_to_MessageType('Generic'))

    def test_message_type_to_MessageType_throws_if_type_is_not_call_or_generic(self):
        self.assertRaises(Exception, Converters.message_type_to_MessageType, 'ThisTypeDoesNotExist')

    def test_timestamp_to_datetime_returns_expected(self):
        r = Converters.timestamp_to_datetime(1672574400)
        self.assertEqual(datetime.datetime(2023, 1, 1, 13, 0, 0), r)

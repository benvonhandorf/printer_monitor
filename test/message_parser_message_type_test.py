import unittest
from message_parser import MessageParser

class MessageParserMessageTypeTestCase(unittest.TestCase):
    def setUp(self):
        self.under_test = MessageParser('printer')

    def test_temp_message_klipper(self):
        result = self.under_test.parse_message_type('printer/zerogravitas/klipper/state/extruder/temperature')

        self.assertEqual(result, MessageParser.MessageType.TEMP)

    def test_status_message_klipper(self):
        result = self.under_test.parse_message_type('printer/zerogravitas/klipper/state/idle_timeout/state')

        self.assertEqual(result, MessageParser.MessageType.STATUS)

    def test_unknown_message_klipper(self):
        result = self.under_test.parse_message_type('printer/zerogravitas/klipper/state/another_thing/state')

        self.assertEqual(result, None)

    def test_parse_returns_type(self):
        result = self.under_test.parse('printer/zerogravitas/klipper/state/extruder/temperature', bytes('76.2', 'utf-8'))

        self.assertEqual(result['type'], MessageParser.MessageType.TEMP)


if __name__ == '__main__':
    unittest.main()
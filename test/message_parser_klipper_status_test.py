import unittest
from message_parser_klipper import MessageParserKlipper
from message_parser import MessageParser

class MessageParserKlipperStatusTestCase(unittest.TestCase):
    def setUp(self):
        self.under_test = MessageParserKlipper()

    def test_parse_status_message_ready(self):
        result = self.under_test.parse_status_message(bytes('{"eventtime": 104682.73617241, "value": "Ready"}', 'utf-8'))

        self.assertEqual(result, MessageParser.Status.IDLE)

    def test_parse_status_message_printing(self):
        result = self.under_test.parse_status_message(bytes('{"eventtime": 104682.73617241, "value": "Printing"}', 'utf-8'))

        self.assertEqual(result, MessageParser.Status.PRINTING)

    def test_parse_status_message_unknown(self):
        result = self.under_test.parse_status_message(bytes('{"eventtime": 104682.73617241, "value": "Unknown"}', 'utf-8'))

        self.assertEqual(result, None)


if __name__ == '__main__':
    unittest.main()
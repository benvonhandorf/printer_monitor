import unittest
from message_parser import MessageParser

class MessageParserPrinterFirmwareTestCase(unittest.TestCase):
    def setUp(self):
        self.under_test = MessageParser('printer')

    def test_printer_name_for_klipper(self):
        result = self.under_test.parse('printer/zerogravitas/klipper/state/extruder/temperature', bytes('72.36', 'utf-8'))

        self.assertEqual(result['firmware'], 'klipper')

if __name__ == '__main__':
    unittest.main()
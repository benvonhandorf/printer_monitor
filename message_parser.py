import re
from enum import Enum

class MessageParser:
    class MessageType(Enum):
        STATUS = 1,
        TEMP = 2

    class Status(Enum):
        IDLE = 0,
        ACTIVE = 1,
        PRINTING = 2

    MESSAGE_TYPES = [
        (MessageType.TEMP, re.compile(".*/klipper/state/extruder/temperature")),
        (MessageType.STATUS, re.compile(".*/klipper/state/idle_timeout/state"))
    ]


    def __init__(self, prefix):
        self.topic_printer_name_parser = re.compile(f"{prefix}\/(?P<NAME>\w+)\/.*")
        self.topic_printer_firmware_parser = re.compile(f"{prefix}\/\w+\/(?P<FIRMWARE>\w+)\/.*")

    def parse_message_type(self, topic):

        for (type, regex) in MessageParser.MESSAGE_TYPES:
            if regex.match(topic):
                return type
        
        return None

    def parse(self, topic, payload):
        printer_match = self.topic_printer_name_parser.match(topic)
        firmware_match = self.topic_printer_firmware_parser.match(topic)

        type = self.parse_message_type(topic)

        return {
            'printer': printer_match.group('NAME'),
            'firmware': firmware_match.group('FIRMWARE'),
            'type': type
            }



from message_parser import MessageParser
import json

class MessageParserKlipper:

    STATUS_MAPPING = {
        'Ready': MessageParser.Status.IDLE,
        'Printing': MessageParser.Status.PRINTING,
    }

    def __init__(self) -> None:
        pass

    def parse_status_message(self, payload: bytes) -> MessageParser.Status:
        message_string = str(payload, 'utf-8')
        body = json.loads(message_string)
        status_value = body['value']

        if status_value is None:
            return None
        
        status = MessageParserKlipper.STATUS_MAPPING.get(status_value)
        
        return status

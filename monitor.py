from alert_pushover import PushoverAlerts
import paho.mqtt.client as mqtt
import os
import argparse
from message_parser import MessageParser
from message_parser_klipper import MessageParserKlipper

alerters = []
topic = None
mqtt_client = None
message_parser = None
printer_parsers = {}
printer_status = {}

def build_firmware_parser(firmware: str):
    if firmware == 'klipper':
        return MessageParserKlipper()
    else:
        return None

def parse_message(topic: str, payload: bytes):
    global printer_parsers

    message_data = message_parser.parse(topic, payload)

    if message_data is None:
        print(f'Unable to parse message topic {topic}')
        return

    firmware_parser = printer_parsers.get(message_data['printer'])

    if firmware_parser is None:
        firmware_parser = build_firmware_parser(message_data['firmware'])
        printer_parsers[message_data['printer']] = firmware_parser
    
    if firmware_parser is None:
        print(f'Unable to build parser for firmware {message_data["firmware"]}')
        return
    
    if message_data['type'] == MessageParser.MessageType.STATUS:
        new_status = firmware_parser.parse_status_message(payload)
        old_status = printer_status.get(message_data['printer'])

        printer_status[message_data['printer']] = new_status

        if old_status != new_status:
            notification = f'Printer {message_data["printer"]} is now {new_status} (was {old_status})'

            print(notification)

            for alerter in alerters:
                alerter.send_message(notification)
        else:
            print(f'Status unchaged: {new_status}')
            print(message_data)
            print(str(payload, 'utf-8'))


def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))

    global message_parser

    message_parser = MessageParser('printer')

    mqtt_client.subscribe(args.mqtt_topic, 2)

def on_message(client, userdata, message):
    parse_message(message.topic, message.payload)

def on_log(client, userdata, level, buf):
    print("{}: {}", level, buf)

if __name__ == "__main__":
    argument_parser = argparse.ArgumentParser()
    argument_parser.add_argument('--pushover_user_key', default=os.environ.get('PUSHOVER_USER_KEY'),
            help="Pushover User Key or set PUSHOVER_USER_KEY")
    argument_parser.add_argument('--pushover_token', default=os.environ.get('PUSHOVER_TOKEN'),
            help="Pushover Token or set PUSHOVER_TOKEN")
    
    argument_parser.add_argument('--mqtt_host', default=os.environ.get('MQTT_HOST'),
            help="MQTT Host")
    argument_parser.add_argument('--mqtt_port', default=os.environ.get('MQTT_PORT') or 1883,
            help="MQTT Port")
    argument_parser.add_argument('--mqtt_user', default=os.environ.get('MQTT_USER'),
            help="MQTT User")
    argument_parser.add_argument('--mqtt_password', default=os.environ.get('MQTT_PASSWORD'),
            help="MQTT Password")
    argument_parser.add_argument('--mqtt_topic', default=os.environ.get('MQTT_TOPIC'),
            help="MQTT Topic")

    args = argument_parser.parse_args()

    if args.pushover_user_key is not None and args.pushover_token is not None:
        alerters.append(PushoverAlerts(args.pushover_token, args.pushover_user_key))
    
    if not alerters:
        argument_parser.print_usage()
        exit(-1)
    
    mqtt_client = mqtt.Client(client_id='PrinterMonitor')

    # mqtt_client.on_log = on_log
    mqtt_client.on_connect = on_connect
    mqtt_client.on_message=on_message

    mqtt_client.username_pw_set(args.mqtt_user, args.mqtt_password)

    mqtt_client.connect(args.mqtt_host, port=int(args.mqtt_port))

    topic = args.mqtt_topic

    mqtt_client.loop_start()

    while True:
        pass
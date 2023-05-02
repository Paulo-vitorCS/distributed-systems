import paho.mqtt.client as mqtt
from database import Database
import json


db = Database()


class MQTTClient:

    def __init__(self, topic):
        self.topic = topic
        self.broker = "mqtt.eclipseprojects.io"
        self.client = mqtt.Client()
        self.client.connect(self.broker)
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message

    def on_connect(self, client, userdata, flags, rc):
        if rc == 0:
            print('Successful connection with MQTT broker')
            client.subscribe(self.topic)
        else:
            print(f'Failed to connect with MQTT broker {rc}')

    def on_message(self, client, userdata, message):
        str_messages = message.payload.decode().split(';')
        print(f'Topic: {message.topic}/{str_messages[0]} | Message received: {str_messages[1]}')

        msg = json.loads(str_messages[1])

        if str_messages[0] == 'create_client':
            db.clients.update(msg)
        elif str_messages[0] == 'update_client':
            pass
        elif str_messages[0] == 'update_client':
            pass
        elif str_messages[0] == 'delete_client':
            pass
        elif str_messages[0] == 'create_product':
            pass
        elif str_messages[0] == 'update_product':
            pass
        elif str_messages[0] == 'delete_product':
            pass
        elif str_messages[0] == 'create_order':
            pass
        elif str_messages[0] == 'update_order':
            pass
        elif str_messages[0] == 'delete_order':
            pass

    def start(self):
        self.client.loop_start()

    def stop(self):
        self.client.loop_stop()
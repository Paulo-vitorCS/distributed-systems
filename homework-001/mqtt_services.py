import paho.mqtt.client as mqtt
import json
import database as db


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
            db.clients.update(msg)

        elif str_messages[0] == 'delete_client':
            cid = list(msg.keys())
            if cid[0] in db.clients:
                db.clients.pop(cid[0])

        elif str_messages[0] == 'create_product':
            db.products.update(msg)

        elif str_messages[0] == 'update_product':
            db.products.update(msg)

        elif str_messages[0] == 'delete_product':
            pid = list(msg.keys())
            if pid[0] in db.products:
                db.products.pop(pid[0])

        elif str_messages[0] == 'create_order':
            order = list(msg.values())
            order = order[0]

            lst = []

            for i in order['product']:
                d = {"PID": i['PID'], "quantity": i['quantity']}
                lst.append(d)

            data = json.dumps(lst)

            if order['OID'] not in db.orders:
                db.create_order(order['OID'], order['CID'], data)

        elif str_messages[0] == 'update_order':
            order = list(msg.values())
            order = order[0]

            lst_old = []
            lst_new = []

            for i in order['product']:
                d = {"PID": i['PID'], "quantity": i['quantity']}
                lst_old.append(d)

            for i in order['update']:
                d = {"PID": i['PID'], "quantity": i['quantity']}
                lst_new.append(d)

            data = {'OID': order['OID'], 'CID': order['CID'], 'product': lst_old, 'update': lst_new}
            data = json.dumps(data)

            flag = 0
            check_order = json.loads(db.retrieve_order(order['OID']).data)
            check_order = check_order['product']

            for i in range(len(check_order)):
                if check_order[i]['quantity'] != lst_new[i]['quantity']:
                    flag += 1

            if flag > 0:
                db.update_order(order['OID'], order['CID'], data)

        elif str_messages[0] == 'delete_order':
            order = list(msg.values())
            order = order[0]

            check_order = json.loads(db.retrieve_order(order['OID']).data)

            if check_order['OID'] != '0':
                db.delete_order(order['OID'])

    def start(self):
        self.client.loop_start()

    def stop(self):
        self.client.loop_stop()
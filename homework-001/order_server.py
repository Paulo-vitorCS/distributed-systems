from concurrent import futures

from database import Database
import grpc
import logging
import json
import services_pb2
import services_pb2_grpc
import paho.mqtt.client as mqtt


db = Database()


class MQTTClient:
    def __init__(self, topic):
        self.topic = topic
        self.broker = "mqtt.eclipseprojects.io"
        self.client = mqtt.Client()
        self.client.connect(self.broker)
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message
        # self.client.connect("localhost", 1883, 60)

    def on_connect(self, client, userdata, flags, rc):
        print(f"Connected with result code {str(rc)}")
        client.subscribe(self.topic)

    def on_message(self, client, userdata, msg):
        print(f"Received message on topic {msg.topic}: {msg.payload.decode()}\n")
        message = json.loads(msg.payload.decode())
        print(message)
        print(str(message))
        if msg.topic == 'orders':
            print(db.orders.values())
            db.orders.update({message['OID']: str(message)})

    def start(self):
        self.client.loop_start()

    def stop(self):
        self.client.loop_stop()


class OrderPortalServicer(services_pb2_grpc.OrderPortalServicer):

    # def __init__(self):
    #     self.mqtt_client = MQTTClient("orders")
    #     self.mqtt_client.start()

    def CreateOrder(self, request, context):
        try:
            db.create_order(request.OID, request.CID, request.data)
            message = f'The OID: {request.OID} has been added successfully'
            # message2 = f"{request.data}"
            # self.mqtt_client.client.publish('orders', message2)
            return services_pb2.Reply(error=0, description=message)
        except Exception as error:
            return services_pb2.Reply(error=1, description=str(error))

    def RetrieveOrder(self, request, context):
        order, total = db.retrieve_order(request.ID)
        message = "{}\nTotal: RS{:.2f}".format(order['products'], total)
        return services_pb2.Order(OID=order['OID'], CID=order['CID'], data=message)

    def UpdateOrder(self, request, context):
        try:
            db.update_order(request.CID, request.OID, request.data)
            message = f'The OID: {request.OID} was updated successfully'
            return services_pb2.Reply(error=0, description=message)
        except Exception as error:
            return services_pb2.Reply(error=1, description=str(error))

    def DeleteOrder(self, request, context):
        try:
            db.delete_order(request.ID)
            message = f'The OID: {request.ID} was deleted successfully'
            return services_pb2.Reply(error=0, description=message)
        except Exception as error:
            return services_pb2.Reply(error=1, description=str(error))

    def RetrieveClientOrders(self, request, context):
        client_orders = db.retrieve_orders(request.ID)
        for i in client_orders:
            order = services_pb2.Order(OID=i['OID'], CID=i['CID'], data=str(i['products']))
            yield order


def serve():

    port = input('Enter the port: ')
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    services_pb2_grpc.add_OrderPortalServicer_to_server(OrderPortalServicer(), server)
    server.add_insecure_port('[::]:' + port)
    server.start()
    print("Server started, listening on " + port)
    server.wait_for_termination()


if __name__ == '__main__':
    logging.basicConfig()
    serve()

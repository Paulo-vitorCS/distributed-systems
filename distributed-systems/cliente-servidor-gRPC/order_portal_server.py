from concurrent import futures
import logging
import grpc
import admin_pb2
import admin_pb2_grpc
from BD.cliente_DB import ClientDB
from BD.produto_DB import ProdutoDB
from BD.orders_DB import OrdersDB
import paho.mqtt.client as mqtt


clients = ClientDB()
products = ProdutoDB()
orders = OrdersDB()


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
        print(f"Received message on topic {msg.topic}: {msg.payload.decode()}")
        message = msg.payload.split(' ')
        if message[0] == 'insert':
            print(f'{message[1]} {message[2]} {message[3]}')
            # orders.insert(message[1], message[2], message[3])

    def start(self):
        self.client.loop_start()

    def stop(self):
        self.client.loop_stop()


class OrderPortalServicer(admin_pb2_grpc.OrderPortalServicer):

    def __init__(self):
        self.mqtt_client = MQTTClient("orders")
        self.mqtt_client.start()

    def CreateOrder(self, request, context):
        try:
            orders.insert(request.OID, request.CID, request.data)
            message = f'The order {request.data}, OID: {request.OID} has been added'
            message2 = f'insert {request.OID} {request.CID} {request.data}'
            self.mqtt_client.client.publish('orders', message2)
            return admin_pb2.Reply(error=0, description=message)
        except Exception as error:
            return admin_pb2.Reply(error=1, description=str(error))

    def RetrieveOrder(self, request, context):
        order, total = orders.search(request.ID)
        message = "{}\nTotal: RS{:.2f}".format(order['products'], total)
        self.mqtt_client.client.publish('orders', message)
        return admin_pb2.Order(CID=order['CID'], OID=order['OID'], data=message)

    def UpdateOrder(self, request, context):
        try:
            orders.update(request.CID, request.OID, request.data)
            message = f'Order {request.OID} updated successfully'
            self.mqtt_client.client.publish('update', message)
            return admin_pb2.Reply(error=0, description=message)
        except Exception as error:
            return admin_pb2.Reply(error=1, description=str(error))

    def DeleteOrder(self, request, context):
        try:
            orders.remove(request.ID)
            message = f'OID: {request.ID} was removed successfully'
            self.mqtt_client.client.publish('orders', message)
            return admin_pb2.Reply(error=0, description=message)
        except Exception as error:
            return admin_pb2.Reply(error=1, description=str(error))

    def RetrieveClientOrders(self, request, context):
        client_orders = orders.searches(request.ID)
        for i in client_orders:
            order = admin_pb2.Order(OID=i['OID'], CID=i['CID'], data=str(i['products']))
            yield order


def serve():

    port = input('Enter the port: ')
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    admin_pb2_grpc.add_OrderPortalServicer_to_server(OrderPortalServicer(), server)
    server.add_insecure_port('[::]:' + port)
    server.start()
    print("Server started, listening on " + port)
    server.wait_for_termination()


if __name__ == '__main__':
    logging.basicConfig()
    serve()

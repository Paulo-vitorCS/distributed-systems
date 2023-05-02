from concurrent import futures

from database import Database
from mqtt_services import MQTTClient
import grpc
import json
import logging
import services_pb2
import services_pb2_grpc


db = Database()


class OrderPortalServicer(services_pb2_grpc.OrderPortalServicer):

    # def __init__(self):
    #     self.mqtt_client = MQTTClient("orders")
    #     self.mqtt_client.start()

    def CreateOrder(self, request, context):
        try:
            db.create_order(request.OID, request.CID, request.data)
            return services_pb2.Reply(error=0, description=f'The OID:{request.OID} was added successfully')
        except Exception as error:
            return services_pb2.Reply(error=1, description=str(error))

    def RetrieveOrder(self, request, context):
        try:
            return db.retrieve_order(request.ID)
        except Exception as error:
            return services_pb2.Order(OID='0', CID='0', data=str(error))

    def UpdateOrder(self, request, context):
        try:
            db.update_order(request.OID, request.CID, request.data)
            return services_pb2.Reply(error=0, description=f'The OID:{request.OID} was updated successfully')
        except Exception as error:
            return services_pb2.Reply(error=1, description=str(error))

    def DeleteOrder(self, request, context):
        try:
            db.delete_order(request.ID)
            return services_pb2.Reply(error=0, description=f'The OID:{request.ID} was deleted successfully')
        except Exception as error:
            return services_pb2.Reply(error=1, description=str(error))

    def RetrieveClientOrders(self, request, context):
        client_orders = db.retrieve_client_orders(request.ID)

        for aux in client_orders:
            oid = aux['OID']
            cid = aux['CID']
            product = aux['product']
            product = json.dumps(product)

            order = services_pb2.Order(OID=oid, CID=cid, data=product)
            yield order


def serve():

    port = input('Enter the port: ')

    if len(port) == 0:
        port = '50051'

    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    services_pb2_grpc.add_OrderPortalServicer_to_server(OrderPortalServicer(), server)
    server.add_insecure_port('[::]:' + port)
    server.start()
    print("Server started, listening on " + port)
    server.wait_for_termination()


if __name__ == '__main__':
    logging.basicConfig()
    serve()

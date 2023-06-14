# Authors: Pedro H. R. Ribeiro, Paulo V. C. Silva
# Description: Order portal server implementation
# Date: 2023-04-30 - Time: 10:00

from concurrent import futures

import database
import grpc
import json
import logging
import services_pb2
import services_pb2_grpc


class OrderPortalServicer(services_pb2_grpc.OrderPortalServicer):

    def CreateOrder(self, request, context):

        try:
            database.create_order(request.OID, request.CID, request.data)
            return services_pb2.Reply(error=0, description=f'The OID:{request.OID} was added successfully')
        except Exception as error:
            return services_pb2.Reply(error=1, description=str(error))

    def RetrieveOrder(self, request, context):

        try:
            return database.retrieve_order(request.ID)
        except Exception as error:
            return services_pb2.Order(OID='0', CID='0', data=str(error))

    def UpdateOrder(self, request, context):

        try:
            database.update_order(request.OID, request.CID, request.data)
            return services_pb2.Reply(error=0, description=f'The OID:{request.OID} was updated successfully')
        except Exception as error:
            return services_pb2.Reply(error=1, description=str(error))

    def DeleteOrder(self, request, context):

        try:
            info = database.retrieve_order(request.ID)
            database.delete_order(request.ID)
            return services_pb2.Reply(error=0, description=f'The OID:{request.ID} was deleted successfully')
        except Exception as error:
            return services_pb2.Reply(error=1, description=str(error))

    def RetrieveClientOrders(self, request, context):

        client_orders = database.retrieve_client_orders(request.ID)

        for aux in client_orders:

            oid = aux['OID']
            cid = aux['CID']
            product = aux['product']
            product = json.dumps(product)

            order = services_pb2.Order(OID=oid, CID=cid, data=product)
            yield order


def test_clients():
    data = {'CID': '100', 'name': 'Pedro'}
    data = json.dumps(data)
    database.create_client('100', data)
    data = {'CID': '101', 'name': 'Paulo'}
    data = json.dumps(data)
    database.create_client('101', data)


def test_products():
    data = {'PID': '100', 'name': 'product-001', 'quantity': '20', 'price': '1.10'}
    data = json.dumps(data)
    database.create_product('100', data)
    data = {'PID': '101', 'name': 'product-002', 'quantity': '10', 'price': '2.50'}
    data = json.dumps(data)
    database.create_product('101', data)


def serve():

    test_clients()
    test_products()

    port = input('Enter the port: ')

    if len(port) == 0:
        port = '50051'

    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    services_pb2_grpc.add_OrderPortalServicer_to_server(OrderPortalServicer(), server)
    server.add_insecure_port('[::]:' + port)
    server.start()

    print(f'Server started, listening on {port}')

    server.wait_for_termination()


if __name__ == '__main__':

    logging.basicConfig()
    serve()

from concurrent import futures

from database import Database
import grpc
import logging
import services_pb2
import services_pb2_grpc

db = Database()


class OrderPortalServicer(services_pb2_grpc.OrderPortalServicer):

    def CreateOrder(self, request, context):
        try:
            db.create_order(request.OID, request.CID, request.data)
            message = f'The OID: {request.OID} has been added successfully'
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

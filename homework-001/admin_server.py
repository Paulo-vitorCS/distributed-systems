# Authors: Pedro H. R. Ribeiro, Paulo V. C. Silva
# Description: Admin portal implementation
# Date: 2023-04-29 - Time: 16:00

from concurrent import futures

from database import Database
import grpc
import logging
import services_pb2
import services_pb2_grpc

db = Database()


class AdminPortalServicer(services_pb2_grpc.AdminPortalServicer):

    def CreateClient(self, request, context):
        try:
            db.create_client(request.CID, request.data)
            message = f'The CID: {request.CID} was added successfully'
            return services_pb2.Reply(error=0, description=message)
        except Exception as error:
            return services_pb2.Reply(error=1, description=str(error))

    def RetrieveClient(self, request, context):
        return db.retrieve_client(request.ID)

    def UpdateClient(self, request, context):
        try:
            db.update_client(request.CID, request.data)
            message = f'The CID: {request.CID} was updated successfully'
            return services_pb2.Reply(error=0, description=message)
        except Exception as error:
            return services_pb2.Reply(error=1, description=str(error))

    def DeleteClient(self, request, context):
        try:
            db.delete_client(request.ID)
            message = f'The CID: {request.ID} was deleted successfully'
            return services_pb2.Reply(error=0, description=message)
        except Exception as error:
            return services_pb2.Reply(error=1, description=str(error))

    def CreateProduct(self, request, context):
        try:
            db.create_product(request.PID, request.data)
            message = f'The PID: {request.PID} was added successfully'
            return services_pb2.Reply(error=0, description=message)
        except Exception as error:
            return services_pb2.Reply(error=1, description=str(error))

    def RetrieveProduct(self, request, context):
        return db.retrieve_product(request.ID)

    def UpdateProduct(self, request, context):
        try:
            db.update_product(request.PID, request.data)
            message = f'The PID: {request.PID} was updated successfully'
            return services_pb2.Reply(error=0, description=message)
        except Exception as error:
            return services_pb2.Reply(error=1, description=str(error))

    def DeleteProduct(self, request, context):
        try:
            db.delete_product(request.ID)
            message = f'The PID: {request.ID} was deleted successfully'
            return services_pb2.Reply(error=0, description=message)
        except Exception as error:
            return services_pb2.Reply(error=1, description=str(error))


def serve():

    port = input('Enter the port: ')

    if len(port) == 0:
        port = '50051'

    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    services_pb2_grpc.add_AdminPortalServicer_to_server(AdminPortalServicer(), server)
    server.add_insecure_port('[::]:' + port)
    server.start()

    print(f'Server started, listening on {port}')

    server.wait_for_termination()


if __name__ == '__main__':

    logging.basicConfig()
    serve()

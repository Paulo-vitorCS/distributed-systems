# Authors: Pedro H. R. Ribeiro, Paulo V. C. Silva
# Description: Admin portal implementation
# Date: 2023-04-29 - Time: 16:00

from concurrent import futures

import database
import grpc
import json
import logging
import services_pb2
import services_pb2_grpc


class AdminPortalServicer(services_pb2_grpc.AdminPortalServicer):

    def CreateClient(self, request: services_pb2.Client, context):

        try:
            database.create_client(request.CID, request.data)
            return services_pb2.Reply(error=0, description=f'The CID:{request.CID} was added successfully')
        except Exception as error:
            return services_pb2.Reply(error=1, description=str(error))

    def RetrieveClient(self, request, context):

        try:
            return database.retrieve_client(request.ID)
        except Exception as error:
            data = {"CID": "0", "name": ' '}
            data = json.dumps(data)
            return services_pb2.Client(CID='0', data=data)

    def UpdateClient(self, request, context):

        try:
            database.update_client(request.CID, request.data)
            return services_pb2.Reply(error=0, description=f'The CID:{request.CID} was updated successfully')
        except Exception as error:
            return services_pb2.Reply(error=1, description=str(error))

    def DeleteClient(self, request, context):

        try:
            response = database.retrieve_client(request.ID)
            database.delete_client(request.ID)
            return services_pb2.Reply(error=0, description=f'The CID:{request.ID} was deleted successfully')
        except Exception as error:
            return services_pb2.Reply(error=1, description=str(error))

    def CreateProduct(self, request, context):

        try:
            database.create_product(request.PID, request.data)
            return services_pb2.Reply(error=0, description=f'The PID:{request.PID} was added successfully')
        except Exception as error:
            return services_pb2.Reply(error=1, description=str(error))

    def RetrieveProduct(self, request, context):

        try:
            return database.retrieve_product(request.ID)

        except Exception as error:
            data = {'PID': '0', 'name': ' ', 'quantity': ' ', 'price': ' '}
            data = json.dumps(data)
            return services_pb2.Product(PID='0', data=data)

    def UpdateProduct(self, request, context):

        try:
            database.update_product(request.PID, request.data)
            return services_pb2.Reply(error=0, description=f'The PID:{request.PID} was updated successfully')
        except Exception as error:
            return services_pb2.Reply(error=1, description=str(error))

    def DeleteProduct(self, request, context):

        try:
            response = database.retrieve_product(request.ID)
            database.delete_product(request.ID)
            return services_pb2.Reply(error=0, description=f'The PID:{request.ID} was deleted successfully')
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

# Authors: Pedro H. R. Ribeiro, Paulo V. C. Silva
# Description: Admin portal implementation
# Date: 2023-04-29 - Time: 16:00

from concurrent import futures

import database
import grpc
import logging
import services_pb2
import services_pb2_grpc


class AdminPortalServicer(services_pb2_grpc.AdminPortalServicer):

    def CreateClient(self, request, context):
        return super().CreateClient(request, context)

    def RetrieveClient(self, request, context):
        return super().RetrieveClient(request, context)

    def UpdateClient(self, request, context):
        return super().UpdateClient(request, context)

    def DeleteClient(self, request, context):
        return super().DeleteClient(request, context)

    def CreateProduct(self, request, context):
        return super().CreateProduct(request, context)

    def RetrieveProduct(self, request, context):
        return super().RetrieveProduct(request, context)

    def UpdateProduct(self, request, context):
        return super().UpdateProduct(request, context)

    def DeleteProduct(self, request, context):
        return super().DeleteProduct(request, context)


def serve():

    port = input('Enter the port: ')

    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    services_pb2_grpc.add_AdminPortalServicer_to_server(AdminPortalServicer(), server)
    server.add_insecure_port('[::]:' + port)
    server.start()

    print(f'Server started, listening on {port}')

    server.wait_for_termination()


if __name__ == '__main__':

    logging.basicConfig()
    serve()

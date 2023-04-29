from concurrent import futures
import logging
import grpc
import admin_pb2
import admin_pb2_grpc
from BD.cliente_DB import ClientDB
from BD.produto_DB import ProdutoDB

clients = ClientDB()
products = ProdutoDB()


class AdminPortalServicer(admin_pb2_grpc.AdminPortalServicer):
    def CreateClient(self, request: admin_pb2.Client, context):
        try:
            clients.insert(request.data, request.CID)
            return admin_pb2.Reply(error=0, description=f'Client {request.data}, CID: {request.CID} was added')
        except Exception as error:
            return admin_pb2.Reply(error=1, description=str(error))

    def RetrieveClient(self, request, context):
        client = clients.search(request.ID)
        return admin_pb2.Client(CID=client['CID'], data=client['name'])

    def UpdateClient(self, request, context):
        try:
            clients.update(request.data, request.CID)
            return admin_pb2.Reply(error=0, description=f'CID: {request.CID} was modified successfully')
        except Exception as error:
            return admin_pb2.Reply(error=1, description=str(error))

    def DeleteClient(self, request, context):
        try:
            clients.remove(request.ID)
            return admin_pb2.Reply(error=0, description=f'CID: {request.ID} was removed successfully')
        except Exception as error:
            return admin_pb2.Reply(error=1, description=str(error))

    def CreateProduct(self, request: admin_pb2.Product, context):
        try:
            products.insert(request.PID, request.data)
            return admin_pb2.Reply(error=0, description=f'PID: {request.PID} was added successfully')
        except Exception as error:
            return admin_pb2.Reply(error=1, description=str(error))

    def RetrieveProduct(self, request, context):
        product = products.search(request.ID)
        dados = product['name'] + ';' + product['quantity'] + ';' + product['price']
        return admin_pb2.Product(PID=product['PID'], data=dados)

    def UpdateProduct(self, request, context):
        try:
            products.update(request.PID, request.data)
            return admin_pb2.Reply(error=0, description=f'PID: {request.PID} was modified successfully')
        except Exception as error:
            return admin_pb2.Reply(error=1, description=str(error))

    def DeleteProduct(self, request, context):
        try:
            products.remove(request.ID)
            return admin_pb2.Reply(error=0, description=f'PID: {request.ID} was removed successfully')
        except Exception as error:
            return admin_pb2.Reply(error=1, description=str(error))


def serve():
    port = input('Enter the port: ')
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    admin_pb2_grpc.add_AdminPortalServicer_to_server(AdminPortalServicer(), server)
    server.add_insecure_port('[::]:' + port)
    server.start()
    print("Server started, listening on " + port)
    server.wait_for_termination()


if __name__ == '__main__':
    logging.basicConfig()
    serve()

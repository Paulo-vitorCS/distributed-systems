from __future__ import print_function

import services_pb2
import services_pb2_grpc
import grpc
import json
import logging


def create_order(stub):
    cid = input('Enter the CID: ')
    oid = input('Enter the OID: ')

    qtd = int(input('Enter the quantity of products: '))

    products = []

    for i in range(1, qtd + 1):
        pid = input('PID: ')
        quantity = input('Quantity: ')
        price = input('Price: ')

        data = {"PID": pid, "quantity": quantity, "price": price}
        products.append(data)

    message = {"OID": oid, "CID": cid,  "products": products}
    str_message = json.dumps(message)

    response = stub.CreateOrder(services_pb2.Order(OID=oid, CID=cid, data=str_message))
    print('Order client received:', response.description)


def retrieve_order(stub):
    cid = input('Enter the CID: ')
    oid = input('Enter the OID: ')

    message = {"CID": cid, "OID": oid}
    str_message = json.dumps(message)

    response = stub.RetrieveOrder(services_pb2.ID(ID=str_message))
    print(f'Products: {response.data}')


def update_order(stub):
    cid = input('Enter the CID: ')
    oid = input('Enter the OID you want to change: ')
    pid = input('Enter the PID you want to change: ')
    qtd = input('Enter the quantity of products to update: ')

    products = []

    for i in range(1, qtd + 1):
        pid = input('PID: ')
        quantity = input('Quantity: ')
        price = input('Price: ')

        data = {"PID": pid, "quantity": quantity, "price": price}
        products.append(data)

    message = {"OID": oid, "CID": cid, "products": products}
    str_message = json.dumps(message)

    response = stub.UpdateOrder(services_pb2.Order(CID=cid, OID=oid, data=str_message))
    print('Order client received: ', response.description)


def delete_order(stub):
    oid = input('OID: ')
    response = stub.DeleteOrder(services_pb2.ID(ID=oid))
    print(f'Order client received: {response.description}')


def retrieve_orders(stub):
    cid = input('CID: ')
    responses = stub.RetrieveClientOrders(services_pb2.ID(ID=cid))

    print(f'Orders:', end=' ')
    for response in responses:
        print(response.OID, end=' | ')
    print('')


def menu():

    print('')

    print(' ---------------------- ')
    print('| ORDER PORTAL OPTIONS |')
    print('|----------------------|')
    print('| 1 - Insert order     |')
    print('| 2 - Update order     |')
    print('| 3 - Search order OID |')
    print('| 4 - Search order CID |')
    print('| 5 - Delete order     |')
    print('| 6 - Exit             |')
    print(' ---------------------- ')

    print('')


def run():

    port = input('Enter the port: ')
    with grpc.insecure_channel('localhost:' + port) as channel:

        stub = services_pb2_grpc.OrderPortalStub(channel)

        while True:

            menu()

            try:

                option = int(input('Enter an option: '))

                print('')

                if option == 1:
                    create_order(stub)
                elif option == 2:
                    update_order(stub)
                elif option == 3:
                    retrieve_order(stub)
                elif option == 4:
                    retrieve_orders(stub)
                elif option == 5:
                    delete_order(stub)
                elif option == 6:
                    print('Exiting order portal')
                    break
                else:
                    print('Invalid option')

            except Exception as ex:
                print(str(ex))


if __name__ == '__main__':
    logging.basicConfig()
    run()
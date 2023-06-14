# Authors: Pedro H. R. Ribeiro, Paulo V. C. Silva
# Description: Order client implementation
# Date: 2023-04-30 - Time: 10:00

from __future__ import print_function

import grpc
import json
import logging

import database
import services_pb2
import services_pb2_grpc


def create_order(stub):

    oid = input('OID: ')
    cid = input('CID: ')

    orders = []

    while True:

        print()
        pid = input('PID: ')
        quantity = input('quantity: ')

        aux = {'PID': pid, 'quantity': quantity}
        orders.append(aux)

        option = input('Do you want to insert another product? (s/n): ')

        if str.lower(option) == 'n':
            print()
            break

    data = json.dumps(orders)
    response = stub.CreateOrder(services_pb2.Order(OID=oid, CID=cid, data=data))
    print('Status:', response.description)


def retrieve_order(stub):

    oid = input('OID: ')
    response = stub.RetrieveOrder(services_pb2.ID(ID=oid))

    if response.OID == '0':
        print('Status: The database does not contains the order')
    else:
        print('Status: The order was found successfully')
        
    print(json.loads(response.data))


def update_order(stub):

    oid = input('OID: ')
    cid = input('CID: ')

    response = stub.RetrieveOrder(services_pb2.ID(ID=oid))
    print('Order:', json.loads(response.data))

    data = json.loads(response.data)
    new_products = []

    if data['OID'] != '0':

        lst_products = data['product']

        for aux in lst_products:

            print()
            print(aux)
            option = input('Do you want to change? (s/n): ')

            if str.lower(option) == 's':
                quantity = input('New quantity: ')
                data_product = {'PID': aux['PID'], 'quantity': quantity}
            else:
                data_product = {'PID': aux['PID'], 'quantity': aux['quantity']}

            new_products.append(data_product)

    else:

        print('Status: The database does not contains the order')
        return

    info = {'OID': oid, 'CID': cid, 'product': data['product'], 'update': new_products}
    info = json.dumps(info)

    print()
    response = stub.UpdateOrder(services_pb2.Order(OID=oid, CID=cid, data=info))
    print('Status:', response.description)


def delete_order(stub):

    oid = input('OID: ')
    response = stub.DeleteOrder(services_pb2.ID(ID=oid))
    print('Status:', response.description)


def retrieve_client_orders(stub):

    cid = input('CID: ')
    responses = stub.RetrieveClientOrders(services_pb2.ID(ID=cid))

    print('> Client orders:')

    for response in responses:
        info = {"OID": response.OID, "CID": response.CID, "product": json.loads(response.data)}
        print(info)


def menu():

    print('')

    print(' ---------------------------- ')
    print('|    ORDER PORTAL OPTIONS    |')
    print('|----------------------------|')
    print('| 1 - Create order           |')
    print('| 2 - Retrieve order         |')
    print('| 3 - Update order           |')
    print('| 4 - Delete order           |')
    print('| 5 - Retrieve client orders |')
    print('| 6 - Exit                   |')
    print(' ---------------------------- ')

    print('')


def run():

    port = input('Enter the port: ')

    if len(port) == 0:
        port = '50051'

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
                    retrieve_order(stub)
                elif option == 3:
                    update_order(stub)
                elif option == 4:
                    delete_order(stub)
                elif option == 5:
                    retrieve_client_orders(stub)
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

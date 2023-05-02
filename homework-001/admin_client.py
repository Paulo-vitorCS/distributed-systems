# Authors: Pedro H. R. Ribeiro, Paulo V. C. Silva
# Description: Admin client implementation
# Date: 2023-04-29 - Time: 16:00

from __future__ import print_function

import database
import grpc
import json
import logging
import services_pb2
import services_pb2_grpc


def create_client(stub):
    cid = input('CID: ')
    name = input('Name: ')
    data = json.dumps({'CID': cid, 'name': name})
    response = stub.CreateClient(services_pb2.Client(CID=cid, data=data))
    print('Admin client received:', response.description)


def retrieve_client(stub):
    cid = input('CID: ')
    response = stub.RetrieveClient(services_pb2.ID(ID=cid))
    if response.CID == '0':
        print('The database does not contains the client')
    else:
        print('The client was found successfully')
    print(json.loads(response.data))


def update_client(stub):
    cid = input('CID: ')
    name = input('Enter a new name: ')
    data = json.dumps({'CID': cid, 'name': name})
    response = stub.UpdateClient(services_pb2.Client(CID=cid, data=data))
    print('Admin client received:', response.description)


def delete_client(stub):
    cid = input('CID: ')
    response = stub.DeleteClient(services_pb2.ID(ID=cid))
    print('Admin client received:', response.description)


def create_product(stub):
    pid = input('PID: ')
    name = input('Name: ')
    quantity = input('Quantity: ')
    price = input('Price: ')
    data = {'PID': pid, 'name': name, 'quantity': quantity, 'price': price}
    data = json.dumps(data)
    response = stub.CreateProduct(services_pb2.Product(PID=pid, data=data))
    print('Admin client received:', response.description)


def retrieve_product(stub):
    pid = input('PID: ')
    response = stub.RetrieveProduct(services_pb2.ID(ID=pid))
    if response.PID == '0':
        print('The database does not contains the product')
    else:
        print('The product was found successfully')
    print(json.loads(response.data))


def update_product(stub):
    pid = input('PID: ')
    name = input('New name: ')
    quantity = input('New quantity: ')
    price = input('New price: ')
    data = {'PID': pid, 'name': name, 'quantity': quantity, 'price': price}
    data = json.dumps(data)
    response = stub.UpdateProduct(services_pb2.Product(PID=pid, data=data))
    print('Admin client received:', response.description)


def delete_product(stub):
    pid = input('PID: ')
    response = stub.DeleteProduct(services_pb2.ID(ID=pid))
    print('Admin client received:', response.description)


def menu_clients():

    print('')

    print(' ---------------------- ')
    print('| ADMIN PORTAL OPTIONS |')
    print('|----------------------|')
    print('| 1 - Insert client    |')
    print('| 2 - Update client    |')
    print('| 3 - Search client    |')
    print('| 4 - Remove client    |')
    print('| 5 - Back             |')
    print(' ---------------------- ')

    print('')


def menu_products():

    print('')

    print(' ---------------------- ')
    print('| ADMIN PORTAL OPTIONS |')
    print('|----------------------|')
    print('| 1 - Insert product   |')
    print('| 2 - Update product   |')
    print('| 3 - Search product   |')
    print('| 4 - Remove product   |')
    print('| 5 - Back             |')
    print(' ---------------------- ')

    print('')


def menu():

    print('')

    print(' ---------------------- ')
    print('| ADMIN PORTAL OPTIONS |')
    print('|----------------------|')
    print('| 1 - Client options   |')
    print('| 2 - Product options  |')
    print('| 3 - Exit             |')
    print(' ---------------------- ')

    print('')


def client_options(stub):

    while True:
        menu_clients()
        try:
            option = int(input('Enter an option: '))
            print('')
            if option == 1:
                create_client(stub)
            elif option == 2:
                update_client(stub)
            elif option == 3:
                retrieve_client(stub)
            elif option == 4:
                delete_client(stub)
            elif option == 5:
                print('Exiting client options')
                break
            else:
                print('Invalid option')
        except Exception as ex:
            print(str(ex))


def product_options(stub):

    while True:
        menu_products()
        try:
            option = int(input('Enter an option: '))
            print('')
            if option == 1:
                create_product(stub)
            elif option == 2:
                update_product(stub)
            elif option == 3:
                retrieve_product(stub)
            elif option == 4:
                delete_product(stub)
                pass
            elif option == 5:
                print('Exiting product options')
                break
            else:
                print('Invalid option')
        except Exception as ex:
            print(str(ex))


def run():

    port = input('Enter the port: ')

    if len(port) == 0:
        port = '50051'

    with grpc.insecure_channel('localhost:' + port) as channel:
        stub = services_pb2_grpc.AdminPortalStub(channel)

        while True:
            menu()

            try:
                option = int(input('Option: '))

                if option == 1:
                    client_options(stub)
                elif option == 2:
                    product_options(stub)
                elif option == 3:
                    print('\nFinished successfully\n')
                    break
                else:
                    print('Invalid option')

            except Exception as ex:

                print(str(ex))


if __name__ == '__main__':

    logging.basicConfig()
    run()

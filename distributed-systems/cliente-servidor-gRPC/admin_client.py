from __future__ import print_function

import json
import logging
import grpc
import admin_pb2
import admin_pb2_grpc


def insert_client(stub):

    name = input('Name: ')
    cid = input('CID: ')
    response = stub.CreateClient(admin_pb2.Client(CID=cid, data=name))
    print('Message: ', response.description)


def update_client(stub):
    cid = input('Enter the CID to update: ')
    name = input('Enter the new name: ')
    response = stub.UpdateClient(admin_pb2.Client(CID=cid, data=name))
    print('Message: ', response.description)


def search_client(stub):
    cid = input('CID: ')
    response = stub.RetrieveClient(admin_pb2.ID(ID=cid))
    print(f'Client: {response.data} \nCID: {response.CID}')


def remove_client(stub):
    cid = input('CID: ')
    response = stub.DeleteClient(admin_pb2.ID(ID=cid))
    print('Message: ', response.description)


def insert_product(stub):
    pid = input('PID: ')
    name = input('Name: ')
    quantity = input('Quantity: ')
    price = input('Price: ')
    dados = {"name": name, "quantity": quantity, "price": price}
    response = stub.CreateProduct(admin_pb2.Product(PID=pid, data=str(json.dumps(dados))))
    print('Message: ', response.description)


def update_product(stub):
    pid = input('Enter the PID to update: ')
    name = input('Enter the new name: ')
    quantity = input('Enter the quantity: ')
    price = input('Enter the new price: ')
    dados = {"name": name, "quantity": quantity, "price": price}
    response = stub.UpdateProduct(admin_pb2.Product(PID=pid, data=str(json.dumps(dados))))
    print('Message: ', response.description)


def search_product(stub):
    pid = input('PID: ')
    response = stub.RetrieveProduct(admin_pb2.ID(ID=pid))
    dados = response.data.split(';')
    print(f'Product: {dados[0]} \nQuantity: {dados[1]}'
          f'\nPrice: {dados[2]} \nPID: {response.PID}')


def remove_product(stub):
    pid = input('PID: ')
    response = stub.DeleteProduct(admin_pb2.ID(ID=pid))
    print('Message: ', response.description)


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
                insert_client(stub)
            elif option == 2:
                update_client(stub)
            elif option == 3:
                search_client(stub)
            elif option == 4:
                remove_client(stub)
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
                insert_product(stub)
            elif option == 2:
                update_product(stub)
            elif option == 3:
                search_product(stub)
            elif option == 4:
                remove_product(stub)
            elif option == 5:
                print('Exiting product options')
                break
            else:
                print('Invalid option')
        except Exception as ex:
            print(str(ex))


def run():

    port = input('Enter the port: ')

    with grpc.insecure_channel('localhost:' + port) as channel:

        stub = admin_pb2_grpc.AdminPortalStub(channel)

        while True:
            menu()
            try:
                option = int(input('Enter an option: '))
                if option == 1:
                    client_options(stub)
                elif option == 2:
                    product_options(stub)
                elif option == 3:
                    print('\nExiting order portal')
                    break
                else:
                    print('Invalid option')
            except Exception as ex:
                print(str(ex))


if __name__ == '__main__':
    logging.basicConfig()
    run()

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
                # insert_client(stub)
                pass
            elif option == 2:
                # update_client(stub)
                pass
            elif option == 3:
                # search_client(stub)
                pass
            elif option == 4:
                # remove_client(stub)
                pass
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
                # insert_product(stub)
                pass
            elif option == 2:
                # update_product(stub)
                pass
            elif option == 3:
                # search_product(stub)
                pass
            elif option == 4:
                # remove_product(stub)
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

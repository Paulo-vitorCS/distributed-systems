# Authors: Pedro H. R. Ribeiro, Paulo V. C. Silva
# Description: Database implementation
# Date: 2023-04-29 - Time: 16:00

from __future__ import print_function
from db_pysyncobj import Database

import sys
import socket
import threading
import json


def controller(instance, conn, addr):
    while True:
        data = conn.recv(1024)
        message = data.decode()

        command_name = None
        key = None
        value = None
        answer = None

        if message:
            response_msg = json.loads(message)
            command_name = response_msg['command']
            key = response_msg['key']
            value = response_msg['value']

        if command_name == 'insert':
            instance.insert_data(key, value)
            answer = json.dumps({'message': 'ok'})

        if command_name == 'update':
            instance.update_data(key, value)
            answer = json.dumps({'message': 'ok'})

        if command_name == 'retrieve':
            response = instance.get_data(key)
            if response:
                response = json.loads(response)
            answer = json.dumps({'data': response})

        if command_name == 'delete':
            instance.delete_data(key)
            answer = json.dumps({'message': 'ok'})

        if command_name == 'retrieve_client_orders':
            response = instance.get_client_orders_data(key)
            answer = json.dumps({'data': response})

        conn.send(answer.encode())


def run():
    socket_port = None
    instance = None

    if len(sys.argv) < 2:
        sys.exit(-1)

    arg = int(sys.argv[1])

    if arg not in range(1, 7):
        print("Outside the range of instances")
        sys.exit(-1)

    # Partition 001
    if arg == 1:
        socket_port = 5000
        instance = Database(socket_port, 'partition_001', 'localhost:6000', ['localhost:6002', 'localhost:6004'])
    if arg == 2:
        socket_port = 5002
        instance = Database(socket_port, 'partition_001', 'localhost:6002', ['localhost:6000', 'localhost:6004'])
    if arg == 3:
        socket_port = 5004
        instance = Database(socket_port, 'partition_001', 'localhost:6004', ['localhost:6000', 'localhost:6002'])

    # Partition 002
    if arg == 4:
        socket_port = 5001
        instance = Database(socket_port, 'partition_002', 'localhost:6001', ['localhost:6003', 'localhost:6005'])
    if arg == 5:
        socket_port = 5003
        instance = Database(socket_port, 'partition_002', 'localhost:6003', ['localhost:6001', 'localhost:6005'])
    if arg == 6:
        socket_port = 5005
        instance = Database(socket_port, 'partition_002', 'localhost:6005', ['localhost:6001', 'localhost:6003'])

    s = socket.socket()
    host = socket.gethostname()
    s.bind((host, socket_port))
    s.listen(12)

    while True:
        conn, addr = s.accept()
        threading.Thread(target=controller, args=(instance, conn, addr)).start()


if __name__ == '__main__':
    run()

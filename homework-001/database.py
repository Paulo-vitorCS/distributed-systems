# Authors: Pedro H. R. Ribeiro, Paulo V. C. Silva
# Description: Database implementation
# Date: 2023-04-29 - Time: 16:00
import json

import services_pb2


class Database:

    def __init__(self):
        self.clients = {}
        self.products = {}
        self.orders = {}
        self.load_initial_db()

    def create_client(self, cid, data):
        if cid in self.clients:
            raise Exception('The database alrealdy contains the client ID')
        else:
            data = json.loads(data)
            self.clients.update({cid: data})
            print(self.clients)

    def retrieve_client(self, cid):
        if cid in self.clients:
            data = json.dumps(self.clients[cid])
            return services_pb2.Client(CID=cid, data=data)
        else:
            data = json.dumps({'CID': '0', 'name': ''})
            return services_pb2.Client(CID='0', data=data)

    def update_client(self, cid, data):
        if cid not in self.clients:
            raise Exception('The database does not contains the client ID')
        else:
            data = json.loads(data)
            self.clients.update({cid: data})
            print(self.clients)

    def delete_client(self, cid):
        if cid not in self.clients:
            raise Exception('The database does not contains the client ID')
        else:
            self.clients.pop(cid)
            print(self.clients)

    def create_product(self, pid, data):
        if pid in self.products:
            raise Exception('The database alrealdy contains the product ID')
        else:
            data = json.loads(data)
            self.products.update({pid: data})
            print(self.products)

    def retrieve_product(self, pid):
        if pid in self.products:
            data = json.dumps(self.products[pid])
            return services_pb2.Product(PID=pid, data=data)
        else:
            data = json.dumps({'PID': '0', 'name': '', 'quantity': '', 'price': ''})
            return services_pb2.Product(PID='0', data=data)

    def update_product(self, pid, data):
        if pid not in self.products:
            raise Exception('The database does not contains the product ID')
        else:
            data = json.loads(data)
            self.products.update({pid: data})
            print(self.products)

    def delete_product(self, pid):
        if pid not in self.products:
            raise Exception('The database does not contains the product ID')
        else:
            self.clients.pop(pid)
            print(self.clients)

    def create_order(self, oid, cid, data):
        if cid in self.clients:
            if oid in self.orders:
                raise Exception("The database already contains the entered OID")
            else:
                data = json.loads(data)
                self.orders.update({oid: data})
                print(self.orders)
        else:
            raise Exception("The client ID does not exist in database")

    def retrieve_order(self, message):
        info = json.loads(message)
        cid = info['CID']
        oid = info['OID']
        total = 0

        data = dict(*[value for value in self.orders.values() if value['CID'] == cid and value['OID'] == oid])

        if data:
            for aux in data['products']:
                total += float(aux['quantity']) * float(aux['price'])
            return data, total
        else:
            return {"OID": "0", "CID": "0", "products": '[]'}, total

    def update_order(self, cid, oid, data):
        try:
            if cid in self.clients:
                if oid in self.orders:
                    data = json.loads(data)
                    self.orders.update({oid: data})
                    print(self.orders)
                else:
                    raise Exception('The database does not contains the order ID')
            else:
                raise Exception('The database does not contains the client ID')
        except Exception as error:
            raise Exception(str(error))

    def delete_order(self, oid):
        if oid not in self.orders:
            raise Exception('The database does not contains the order ID')
        else:
            self.orders.pop(oid)
            print(self.orders)

    def retrieve_orders(self, cid):
        order_list = []
        for value in self.orders.values():
            if value['CID'] == cid:
                order_list.append(value)
        return order_list

    def load_initial_db(self):
        self.clients = {
            '100': {'CID': '100', 'name': 'Paulo'},
            '101': {'CID': '101', 'name': 'Ana'},
            '102': {'CID': '102', 'name': 'Pedro'},
            '103': {'CID': '103', 'name': 'Maria'},
            '104': {'CID': '104', 'name': 'José'}
        }

        self.products = {
            '200': {'PID': '200', 'name': 'product_A', 'quantity': '50', 'price': '1.00'},
            '201': {'PID': '201', 'name': 'product_B', 'quantity': '50', 'price': '2.00'},
            '202': {'PID': '202', 'name': 'product_C', 'quantity': '50', 'price': '3.00'},
            '203': {'PID': '203', 'name': 'product_D', 'quantity': '50', 'price': '4.00'}
        }

        self.orders = {'300': {"OID": "300", "CID": "101",
                               "products": [
                                   {"PID": "200", "quantity": "10", "price": "1.00"},
                                   {"PID": "201", "quantity": "15", "price": "2.00"},
                                   {"PID": "202", "quantity": "20", "price": "3.00"}
                               ]},
                       "301": {"OID": "301", "CID": "102",
                               "products": [
                                   {"PID": "202", "quantity": "25", "price": "3.00"},
                                   {"PID": "203", "quantity": "30", "price": "4.00"}
                               ]},
                       "302": {"OID": "302", "CID": "101",
                               "products": [
                                   {"PID": "200", "quantity": "35", "price": "1.00"},
                                   {"PID": "201", "quantity": "40", "price": "2.00"},
                                   {"PID": "202", "quantity": "45", "price": "3.00"},
                                   {"PID": "203", "quantity": "50", "price": "4.00"}
                               ]}
                       }

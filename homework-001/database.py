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

    # ------------------ Clients Database ------------------ #

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

    # ------------------ Products Database ------------------ #

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

    # ------------------ Orders Database ------------------ #

    def create_order(self, oid, cid, data):
        if oid not in self.orders and cid in self.clients:
            data = json.loads(data)
            lst_products = []

            print('> Updating products list')

            for aux in data:
                if aux['PID'] not in self.products:
                    raise Exception(f'The database does not contains PID:{aux["PID"]} product')

                product = self.products[aux['PID']]

                if int(product['quantity']) >= int(aux['quantity']):
                    new_quantity = str(int(product['quantity']) - int(aux['quantity']))
                    data_product = {'PID': aux['PID'], 'name': product['name'], 'quantity': new_quantity,
                                    'price': product['price']}
                    data_product = json.dumps(data_product)
                    self.update_product(aux['PID'], data_product)

                    data_order = {'PID': aux['PID'], 'name': product['name'], 'quantity': aux['quantity'],
                                  'price': product['price']}
                    lst_products.append(data_order)

            if len(lst_products) == 0:
                raise Exception('No order was placed')

            data = {'OID': oid, 'CID': cid, 'product': lst_products}
            self.orders.update({oid: data})

            print('> Orders list')
            print(self.orders)
        else:
            raise Exception('The database already contains the order')

    def retrieve_order(self, oid):
        print('> Retrieving request')

        if oid in self.orders:
            data = self.orders[oid]
            cid = data['CID']
            print(data)
            data = json.dumps(data)
            order = services_pb2.Order(OID=oid, CID=cid, data=data)
            return order
        else:
            data = {"OID": "0", "CID": "0", "products": []}
            print(data)
            data = json.dumps(data)
            return services_pb2.Order(OID='0', CID='0', data=data)

    def update_order(self, oid, cid, data):
        data = json.loads(data)
        old_order = data['product']
        new_order = data['update']

        print('> Updating products quantity')

        for i in range(len(old_order)):

            old = old_order[i]
            new = new_order[i]
            aux_product = self.products[old['PID']]

            if old['quantity'] != new['quantity']:
                new_quantity = str(int(old['quantity']) + int(aux_product['quantity']))
                info = {"PID": old['PID'], "name": old['name'], "quantity": new_quantity, "price": old['price']}
                info = json.dumps(info)
                self.update_product(old['PID'], info)

        # Updating order
        lst_order = []

        for i in range(len(new_order)):
            old = old_order[i]
            new = new_order[i]

            if old['quantity'] != new['quantity'] and int(new['quantity']) > 0:
                product = self.products[new['PID']]

                if int(product['quantity']) >= int(new['quantity']):
                    new_quantity = str(int(product['quantity']) - int(new['quantity']))
                    info = {"PID": new['PID'], "name": product['name'], "quantity": new_quantity,
                            "price": product['price']}
                    info = json.dumps(info)
                    self.update_product(new['PID'], info)
                    info = {"PID": new['PID'], "name": product['name'], "quantity": new['quantity'],
                            "price": product['price']}
                    lst_order.append(info)

            elif old['quantity'] == new['quantity'] and int(new['quantity']) > 0:
                lst_order.append(old)

        if len(lst_order) == 0:
            self.orders[oid] = {"OID": oid, "CID": cid, "product": []}
            self.delete_order(oid)
            raise Exception('Order deleted due to update error or order is empty')

        data = {'OID': oid, 'CID': cid, 'product': lst_order}
        self.orders.update({oid: data})

        print('> Orders list')
        print(self.orders)

    def delete_order(self, oid):
        print('> Updating products list')

        if oid in self.orders:
            lst_products = self.orders[oid]
            lst_products = lst_products['product']

            for aux in lst_products:
                data_product = self.products[aux['PID']]
                new_quantity = str(int(aux['quantity']) + int(data_product['quantity']))
                new_data = {'PID': aux['PID'], 'name': data_product['name'], 'quantity': new_quantity,
                            'price': data_product['price']}
                new_data = json.dumps(new_data)
                self.update_product(aux['PID'], new_data)

            print(self.products)

            print('> Deleting order')
            self.orders.pop(oid)
            print(self.orders)
        else:
            raise Exception('The database does not contains the order')

    def retrieve_client_orders(self, cid):
        lst_orders = []

        for key, value in self.orders.items():
            if value['CID'] == cid:
                lst_orders.append(value)

        return lst_orders

    # ------------------ Data for loading ------------------ #

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
            '203': {'PID': '203', 'name': 'product_D', 'quantity': '50', 'price': '4.00'},
            '204': {'PID': '204', 'name': 'product_E', 'quantity': '50', 'price': '5.00'},
            '205': {'PID': '205', 'name': 'product_F', 'quantity': '50', 'price': '6.00'}
        }

        self.orders = {"300": {"OID": "300", "CID": "101",
                               "product": [
                                   {"PID": "200", "name": "product_A", "quantity": "10", "price": "1.00"},
                                   {"PID": "201", "name": "product_B", "quantity": "15", "price": "2.00"},
                                   {"PID": "202", "name": "product_C", "quantity": "20", "price": "3.00"}
                               ]},
                       "301": {"OID": "301", "CID": "102",
                               "product": [
                                   {"PID": "202", "name": "product_C", "quantity": "25", "price": "3.00"},
                                   {"PID": "203", "name": "product_D", "quantity": "30", "price": "4.00"}
                               ]},
                       "302": {"OID": "302", "CID": "101",
                               "product": [
                                   {"PID": "200", "name": "product_A", "quantity": "35", "price": "1.00"},
                                   {"PID": "201", "name": "product_B", "quantity": "40", "price": "2.00"},
                                   {"PID": "202", "name": "product_C", "quantity": "45", "price": "3.00"},
                                   {"PID": "203", "name": "product_D", "quantity": "50", "price": "4.00"}
                               ]}
                       }

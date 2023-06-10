# Authors: Pedro H. R. Ribeiro, Paulo V. C. Silva
# Description: Database implementation
# Date: 2023-04-29 - Time: 16:00
import json

import services_pb2


# ------------------ Data for loading ------------------ #
def load_initial_db():
    lst_clients = {
        '100': {'CID': '100', 'name': 'Paulo'},
        '101': {'CID': '101', 'name': 'Ana'},
        '102': {'CID': '102', 'name': 'Pedro'},
        '103': {'CID': '103', 'name': 'Maria'},
        '104': {'CID': '104', 'name': 'José'}
    }

    lst_products = {
        '200': {'PID': '200', 'name': 'product_A', 'quantity': '50', 'price': '1.00'},
        '201': {'PID': '201', 'name': 'product_B', 'quantity': '50', 'price': '2.00'},
        '202': {'PID': '202', 'name': 'product_C', 'quantity': '50', 'price': '3.00'},
        '203': {'PID': '203', 'name': 'product_D', 'quantity': '50', 'price': '4.00'},
        '204': {'PID': '204', 'name': 'product_E', 'quantity': '50', 'price': '5.00'},
        '205': {'PID': '205', 'name': 'product_F', 'quantity': '50', 'price': '6.00'}
    }

    lst_orders = {"300": {"OID": "300", "CID": "101",
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

    return lst_clients, lst_products, lst_orders


clients, products, orders = load_initial_db()


# ------------------ Clients Database ------------------ #
def create_client(cid, data):
    if cid in clients:
        raise Exception('The database alrealdy contains the client ID')
    else:
        data = json.loads(data)
        clients.update({cid: data})
        print(clients)


def retrieve_client(cid):
    if cid in clients:
        data = json.dumps(clients[cid])
        return services_pb2.Client(CID=cid, data=data)
    else:
        data = json.dumps({'CID': '0', 'name': ''})
        return services_pb2.Client(CID='0', data=data)


def update_client(cid, data):
    if cid not in clients:
        raise Exception('The database does not contains the client ID')
    else:
        data = json.loads(data)
        clients.update({cid: data})
        print(clients)


def delete_client(cid):
    if cid not in clients:
        raise Exception('The database does not contains the client ID')
    else:
        clients.pop(cid)
        print(clients)


# ------------------ Products Database ------------------ #

def create_product(pid, data):
    if pid in products:
        raise Exception('The database alrealdy contains the product ID')
    else:
        data = json.loads(data)
        products.update({pid: data})
        print(products)


def retrieve_product(pid):
    if pid in products:
        data = json.dumps(products[pid])
        return services_pb2.Product(PID=pid, data=data)
    else:
        data = json.dumps({'PID': '0', 'name': '', 'quantity': '', 'price': ''})
        return services_pb2.Product(PID='0', data=data)


def update_product(pid, data):
    if pid not in products:
        raise Exception('The database does not contains the product ID')
    else:
        data = json.loads(data)
        products.update({pid: data})
        print(products)


def delete_product(pid):
    if pid not in products:
        raise Exception('The database does not contains the product ID')
    else:
        clients.pop(pid)
        print(clients)


# ------------------ Orders Database ------------------ #

def create_order(oid, cid, data):
    if oid not in orders and cid in clients:
        data = json.loads(data)
        lst_products = []

        print('> Updating products list')

        for aux in data:
            if aux['PID'] not in products:
                raise Exception(f'The database does not contains PID:{aux["PID"]} product')

            product = products[aux['PID']]

            if int(product['quantity']) >= int(aux['quantity']):
                new_quantity = str(int(product['quantity']) - int(aux['quantity']))
                data_product = {'PID': aux['PID'], 'name': product['name'], 'quantity': new_quantity,
                                'price': product['price']}
                data_product = json.dumps(data_product)
                update_product(aux['PID'], data_product)

                data_order = {'PID': aux['PID'], 'name': product['name'], 'quantity': aux['quantity'],
                              'price': product['price']}
                lst_products.append(data_order)

        if len(lst_products) == 0:
            raise Exception('No order was placed')

        data = {'OID': oid, 'CID': cid, 'product': lst_products}
        orders.update({oid: data})

        print('> Orders list')
        print(orders)
    else:
        raise Exception('The database already contains the order')


def retrieve_order(oid):
    print('> Retrieving request')

    if oid in orders:
        data = orders[oid]
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


def update_order(oid, cid, data):
    data = json.loads(data)
    old_order = data['product']
    new_order = data['update']

    print('> Updating products quantity')

    for i in range(len(old_order)):

        old = old_order[i]
        new = new_order[i]
        aux_product = products[old['PID']]

        if old['quantity'] != new['quantity']:
            new_quantity = str(int(old['quantity']) + int(aux_product['quantity']))
            info = {"PID": old['PID'], "name": aux_product['name'], "quantity": new_quantity, "price": aux_product['price']}
            info = json.dumps(info)
            update_product(old['PID'], info)

    # Updating order
    lst_order = []

    for i in range(len(new_order)):
        old = old_order[i]
        new = new_order[i]

        if old['quantity'] != new['quantity'] and int(new['quantity']) > 0:
            product = products[new['PID']]

            if int(product['quantity']) >= int(new['quantity']):
                new_quantity = str(int(product['quantity']) - int(new['quantity']))
                info = {"PID": new['PID'], "name": product['name'], "quantity": new_quantity,
                        "price": product['price']}
                info = json.dumps(info)
                update_product(new['PID'], info)
                info = {"PID": new['PID'], "name": product['name'], "quantity": new['quantity'],
                        "price": product['price']}
                lst_order.append(info)

        elif old['quantity'] == new['quantity'] and int(new['quantity']) > 0:
            lst_order.append(old)

    # if len(lst_order) == 0:
    #     orders[oid] = {"OID": oid, "CID": cid, "product": []}
    #     delete_order(oid)
    #     raise Exception('Order deleted due to update error or order is empty')

    data = {'OID': oid, 'CID': cid, 'product': lst_order}
    orders.update({oid: data})

    print('> Orders list')
    print(orders)


def delete_order(oid):
    print('> Updating products list')

    if oid in orders:
        lst_products = orders[oid]
        lst_products = lst_products['product']

        for aux in lst_products:
            data_product = products[aux['PID']]
            new_quantity = str(int(aux['quantity']) + int(data_product['quantity']))
            new_data = {'PID': aux['PID'], 'name': data_product['name'], 'quantity': new_quantity,
                        'price': data_product['price']}
            new_data = json.dumps(new_data)
            update_product(aux['PID'], new_data)

        print(products)

        print('> Deleting order')
        orders.pop(oid)
        print(orders)
    else:
        raise Exception('The database does not contains the order')


def retrieve_client_orders(cid):
    lst_orders = []

    for key, value in orders.items():
        if value['CID'] == cid:
            lst_orders.append(value)

    return lst_orders

# Authors: Pedro H. R. Ribeiro, Paulo V. C. Silva
# Description: Database implementation
# Date: 2023-04-29 - Time: 16:00

import json

import services_pb2

clients = {}
products = {}
orders = {}


def create_client(cid, data):

    if cid not in clients:
        data = json.loads(data)
        clients.update({cid: data})
        print(clients)
    else:
        raise Exception('The database already contains the client')


def retrieve_client(cid):

    if cid in clients:
        data = clients[cid]
        data = json.dumps(data)
        client = services_pb2.Client(CID=cid, data=data)
        return client
    else:
        data = {"CID": "0", "name": ""}
        data = json.dumps(data)
        return services_pb2.Client(CID='0', data=data)


def update_client(cid, data):

    if cid in clients:
        data = json.loads(data)
        clients.update({cid: data})
        print(clients)
    else:
        raise Exception('The database does not contains the client')


def delete_client(cid):

    if cid in clients:
        clients.pop(cid)
        print(clients)
    else:
        raise Exception('The database does not contains the client')


def create_product(pid, data):

    if pid not in products:
        data = json.loads(data)
        products.update({pid: data})
        print(products)
    else:
        raise Exception('The database already contains the product')


def retrieve_product(pid):

    if pid in products:
        data = products[pid]
        data = json.dumps(data)
        product = services_pb2.Product(PID=pid, data=data)
        return product
    else:
        data = {"PID": "0", "name": "", "quantity": "", "price": ""}
        data = json.dumps(data)
        return services_pb2.Product(PID='0', data=data)


def update_product(pid, data):

    if pid in products:
        data = json.loads(data)
        products.update({pid: data})
        print(products)
    else:
        raise Exception('The database does not contains the product')


def delete_product(pid):

    if pid in products:
        products.pop(pid)
        print(products)
    else:
        raise Exception('The database does not contains the product')


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
                data_product = {'PID': aux['PID'], 'name': product['name'], 'quantity': new_quantity, 'price': product['price']}
                data_product = json.dumps(data_product)
                update_product(aux['PID'], data_product)

                data_order = {'PID': aux['PID'], 'name': product['name'], 'quantity': aux['quantity'], 'price': product['price']}
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
                info = {"PID": new['PID'], "name": product['name'], "quantity": new_quantity, "price": product['price']}
                info = json.dumps(info)
                update_product(new['PID'], info)
                info = {"PID": new['PID'], "name": product['name'], "quantity": new['quantity'], "price": product['price']}
                lst_order.append(info)

        elif old['quantity'] == new['quantity'] and int(new['quantity']) > 0:
            lst_order.append(old)

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
            new_data = {'PID': aux['PID'], 'name': data_product['name'], 'quantity': new_quantity, 'price': data_product['price']}
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

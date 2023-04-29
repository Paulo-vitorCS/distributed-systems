import json
from BD.orders_clients_DB import OrderClientDB
from BD.orders_products_DB import OrderProductDB

clients = OrderClientDB()
products = OrderProductDB()


class OrdersDB:

    def __init__(self):
        with open('../JSON/orders.json') as f:
            self.__orders = json.load(f)

    def insert(self, oid, cid, data):

        flag_cid = dict(*[client for client in clients.clients if client['CID'] == cid])
        flag_oid = dict(*[value for value in self.__orders if value['OID'] == oid])

        if flag_cid:
            if flag_oid:
                raise Exception("The database already contains the entered OID")
            else:
                info = json.loads(data)
                if [value for value in self.__orders if value['OID'] != oid]:
                    self.__orders.append({'OID': info['OID'], 'CID': cid, 'products': info['products']})
                    print(self.__orders)
        else:
            raise Exception("The client does not exist in database")

    def update(self, cid, oid, data):

        flag_cid = dict(*[client for client in clients.clients if client['CID'] == cid])
        flag_oid = dict(*[value for value in self.__orders if value['OID'] == oid])

        try:

            if flag_cid and flag_oid:

                info = json.loads(data)

                for aux_orders in self.__orders:
                    for aux_products in aux_orders['products']:
                        if aux_products['PID'] == info['PID']:
                            aux_products['quantity'] = info['quantity']

                print(self.__orders)

            else:
                raise Exception('The order does not exists in the database')

        except Exception as error:
            raise Exception(str(error))

    def search(self, message):
        info = json.loads(message)

        cid = info['CID']
        oid = info['OID']
        total = 0

        data = dict(*[value for value in self.__orders if value['CID'] == cid and value['OID'] == oid])

        if data:
            for aux in data['products']:
                total += float(aux['quantity']) * float(aux['price'])
            return data, total
        else:
            return {"OID": "0", "CID": "0", "products": '[]'}, total

    def remove(self, message):

        info = json.loads(message)

        cid = info['CID']
        oid = info['OID']

        flag_cid = dict(*[client for client in clients.clients if client['CID'] == cid])

        if flag_cid:

            try:
                index = self.__orders.index(*[order for order in self.__orders if order['OID'] == oid])
            except Exception:
                raise Exception("The database does not contain the entered PID")
            else:
                self.__orders.pop(index)
                print(self.__orders)

    def searches(self, cid):
        order_list = []
        for order in self.__orders:
            if order['CID'] == cid:
                order_list.append(order)
        return order_list

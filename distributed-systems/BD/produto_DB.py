import json


class ProdutoDB:
    def __init__(self):
        with open('../JSON/produto.json') as f:
            self.__products = json.load(f)

    def insert(self, pid, data):
        if [prod for prod in self.__products if prod['PID'] == pid]:
            raise Exception("The database already contains the entered PID")
        else:
            info = json.loads(data)
            self.__products.append({'PID': pid, 'name': info['name'],
                                    'quantity': info['quantity'], 'price': info['price']})
            print(self.__products)

    def update(self, pid, data):
        try:
            index = self.__products.index(*[prod for prod in self.__products if prod['PID'] == pid])
        except Exception:
            raise Exception("The database does not contain the entered PID")
        else:
            info = json.loads(data)
            self.__products.pop(index)
            self.__products.insert(index, {'PID': pid, 'name': info['name'],
                                           'quantity': info['quantity'], 'price': info['price']})
            print(self.__products)

    def search(self, pid):
        data = dict(*[prod for prod in self.__products if prod['PID'] == pid])
        if data:
            return data
        return {"PID": "0", "name": "", "quantity": "", "price": ""}

    def remove(self, pid):
        try:
            index = self.__products.index(*[prod for prod in self.__products if prod['PID'] == pid])
        except Exception:
            raise Exception("The database does't contain the entered PID")
        else:
            self.__products.pop(index)
            print(self.__products)

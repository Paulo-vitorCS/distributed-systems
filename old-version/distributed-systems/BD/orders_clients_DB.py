import json


class OrderClientDB:

    def __init__(self):
        with open('../JSON/client.json') as f:
            self.__clients = json.load(f)

    @property
    def clients(self):
        return self.__clients

    def insert(self, name, cid):

        if [client for client in self.__clients if client['CID'] == cid]:
            raise Exception("The database already contains the entered CID")
        else:
            self.__clients.append({'CID': cid, 'name': name})
            print(self.__clients)

    def update(self, name, cid):

        try:
            index = self.__clients.index(*[client for client in self.__clients if client['CID'] == cid])
        except Exception:
            raise Exception("The database does not contain the entered CID")
        else:
            self.__clients.pop(index)
            self.__clients.insert(index, {'CID': cid, 'name': name})
            print(self.__clients)

    def search(self, cid):

        data = dict(*[client for client in self.__clients if client['CID'] == cid])
        if data:
            return data
        return {"CID": "0", "name": ""}

    def remove(self, cid):

        try:
            index = self.__clients.index(*[client for client in self.__clients if client['CID'] == cid])
        except Exception:
            raise Exception("The database does not contain the entered CID")
        else:
            self.__clients.pop(index)
            print(self.__clients)

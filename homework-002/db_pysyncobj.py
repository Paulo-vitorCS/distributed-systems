# Authors: Pedro H. R. Ribeiro, Paulo V. C. Silva
# Description: Database implementation (synchronization)
# Date: 2023-06-12 - Time: 20:00

from pysyncobj import SyncObj, replicated

import plyvel
import json


class Database(SyncObj):
    def __init__(self, port, part, primary, secondary):
        super(Database, self).__init__(primary, secondary)
        self.database = f'./instances/{part}/{port}/'

    @replicated
    def insert_data(self, key, value):
        db = plyvel.DB(self.database, create_if_missing=True)

        print('key:', key, ', value:', value)
        new_key = bytes(key, 'utf-8')
        new_value = bytes(json.dumps(value), 'utf-8')

        db.put(new_key, new_value)

        db.close()

    @replicated
    def delete_data(self, key):
        db = plyvel.DB(self.database, create_if_missing=True)

        print('key:', key)
        new_key = bytes(key, 'utf-8')
        db.delete(new_key)

        db.close()

    def update_data(self, key, value):
        self.delete_data(key)
        self.insert_data(key, value)

    def get_data(self, key):
        db = plyvel.DB(self.database, create_if_missing=True)

        new_key = bytes(key, 'utf-8')

        new_answer = db.get(new_key)

        if new_answer:
            answer = new_answer.decode()
        else:
            answer = None

        db.close()

        return answer

    def get_client_orders_data(self, key):
        db = plyvel.DB(self.database, create_if_missing=True)

        answer = []
        for k, v in db:
            if k.decode()[0] == 'o':
                data = json.loads(v.decode())
                if data['CID'] == key:
                    data = json.dumps(data)
                    answer.append(data)

        return answer

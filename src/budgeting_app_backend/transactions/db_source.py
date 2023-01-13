import pycouchdb


class DbSource:

    def __init__(self, url, name):
        self.__server = pycouchdb.Server(url)
        self.__name = name

    def all(self):
        s = self.__server
        name = self.__name
        db = s.database(name)

        docs = db.all()
        records = [doc['doc'] for doc in docs]

        return records

import pycouchdb


class DbSource:
    def __init__(self, url):
        self.__server = pycouchdb.Server(url)

    def all(self):
        s = self.__server
        db = s.database("budgeting")

        docs = db.all()
        records = [doc["doc"] for doc in docs]

        return records

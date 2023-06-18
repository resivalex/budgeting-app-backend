import pycouchdb
import pandas as pd
import io


class CsvExporting:
    def __init__(self, url):
        self.__server = pycouchdb.Server(url)

    def perform(self):
        db = _get_or_create_database(self.__server, "budgeting")
        records = db.all()
        records = [doc["doc"] for doc in records]
        columns = [
            "datetime",
            "account",
            "category",
            "type",
            "amount",
            "currency",
            "payee",
            "comment",
        ]
        if len(records) == 0:
            df = pd.DataFrame(columns=columns)
        else:
            df = pd.DataFrame(records)
            df = df.drop(columns=["_id", "_rev"])
            df = df.sort_values(by=["datetime"], ascending=False)
            df = df[columns]

        stream = io.StringIO()
        df.to_csv(stream, index=False)

        return stream.getvalue()


def _get_or_create_database(server, db_name):
    if db_name not in server:
        server.create(db_name)
    return server.database(db_name)

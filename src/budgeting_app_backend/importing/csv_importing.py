import pycouchdb
import pandas as pd
import io


class CsvImporting:
    def __init__(self, url):
        self.__server = pycouchdb.Server(url)

    def perform(self, content: bytes):
        text = content.decode("utf8")
        records = _parse_text(text)
        db = _recreate_database(self.__server, "budgeting")
        db.save_bulk(records, transaction=True)
        db.compact()


def _recreate_database(server, db_name):
    if db_name in server:
        server.delete(db_name)
    return server.create(db_name)


def _parse_text(text: str):
    stream = io.StringIO(text)

    return pd.read_csv(stream, dtype=str).fillna("").to_dict(orient="records")

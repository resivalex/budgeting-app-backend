import pycouchdb
import pandas as pd
import io


class CsvImporting:

    def __init__(self, url):
        self.__server = pycouchdb.Server(url)

    def perform(self, content: bytes):
        text = content.decode('utf8')
        records = _parse_text(text)
        s = self.__server
        name = 'budgeting'

        s.delete(name)
        s.create(name)
        db = s.database(name)
        db.save_bulk(records)


def _parse_text(text: str):
    stream = io.StringIO(text)

    return pd.read_csv(stream, dtype=str).fillna('').to_dict(orient='records')

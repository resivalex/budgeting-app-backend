import pycouchdb
import pandas as pd
import io


class CsvImporting:

    def __init__(self, url):
        self.__server = pycouchdb.Server(url)

    def perform(self, content: bytes):
        text = content.decode('utf8')
        records = _parse_text(text)
        db = self.__server.database('budgeting')
        _clear_database(db)
        db.save_bulk(records)


def _clear_database(db):
    docs_to_delete = []
    for row in db.query('_all_docs', include_docs=False):
        docs_to_delete.append({
            '_id': row['id'],
            '_rev': row['value']['rev']
        })

    db.delete_bulk(docs_to_delete)


def _parse_text(text: str):
    stream = io.StringIO(text)

    return pd.read_csv(stream, dtype=str).fillna('').to_dict(orient='records')

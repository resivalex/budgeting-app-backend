import pycouchdb
import pandas as pd
import io


class CsvExporting:

    def __init__(self, url):
        self.__server = pycouchdb.Server(url)

    def perform(self):
        db = self.__server.database('budgeting')
        records = db.all()
        records = [doc['doc'] for doc in records]
        df = pd.DataFrame(records)
        df = df.drop(columns=['_id', '_rev'])
        df = df.sort_values(by=['datetime'], ascending=False)
        df = df[['datetime', 'account', 'category', 'type', 'amount', 'currency', 'payee', 'comment']]

        stream = io.StringIO()
        df.to_csv(stream, index=False)

        return stream.getvalue()

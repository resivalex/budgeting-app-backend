import pandas as pd


class CsvSource:

    def __init__(self, path):
        self.__path = path

    def all(self):
        df = pd.read_csv(self.__path, dtype=str).fillna('')

        return df.to_dict(orient='records')

import psycopg2


class Service:
    def __init__(self):
        self.conn = psycopg2.connect(dbname='dwellingsdb', user='postgres',
                                     password='1111', host='localhost')


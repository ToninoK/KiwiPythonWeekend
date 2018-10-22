import psycopg2
from psycopg2.extras import RealDictCursor
from data_structure import select_tables, insert_table, drop_table, create_table

pg_config = {
    "host": "packy.db.elephantsql.com",
    "database": "hqnuzdkc",
    "user": "hqnuzdkc",
    "password": "gJocf5xtAogBdyOOqMt6EV6OFcVBSCja",
}


class DbController:
    def createTable(self):
        with psycopg2.connect(**pg_config) as conn:
            with conn.cursor(cursor_factory=RealDictCursor) as cur:
                cur.execute(drop_table)
                cur.execute(create_table)

    def getJourneys(self, search):
        with psycopg2.connect(**pg_config) as conn:
            with conn.cursor(cursor_factory=RealDictCursor) as cur:
                cur.execute(
                    select_tables,
                    {"source": search[0], "destination": search[1], "date": search[2]},
                )
                res = cur.fetchall()
                return res

    def saveJourneys(self, data):
        with psycopg2.connect(**pg_config) as conn:
            with conn.cursor(cursor_factory=RealDictCursor) as cur:
                for journey in data:
                    cur.execute(insert_table, journey)
        return data

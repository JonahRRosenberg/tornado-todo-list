
from collections import OrderedDict
import sqlite3

DB_NAME = "mysqlite.db"

# Taken from http://stackoverflow.com/questions/3300464/how-can-i-get-dict-from-sqlite-query
def dict_factory(cursor, row):
    d = OrderedDict()
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d

class DBClient:
    def __init__(self):
        self.conn = sqlite3.connect(DB_NAME)
        self.conn.row_factory = dict_factory
        self.conn.execute('pragma foreign_keys=ON')

    def get_tasks_by_user_id(self, user_id):
        cur = self.conn.execute("SELECT * FROM users WHERE ID = %s" % user_id)
        if cur.fetchone() is None:
            raise RuntimeError("No user found for id: {0}".format(user_id))

        cur = self.conn.execute("SELECT * FROM tasks WHERE user_id = %s" % user_id)
        return cur.fetchall()


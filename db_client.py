
from collections import OrderedDict
from datetime import datetime
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

    def get_tasks_by_user_id(self, user_id, incomplete_only):
        self.__check_is_valid_user(user_id)

        get_tasks_query = "SELECT * FROM tasks WHERE user_id = %s"
        if incomplete_only:
            get_tasks_query += " AND is_complete = 0"

        cur = self.conn.execute(get_tasks_query % user_id)
        return cur.fetchall()

    def create_task(self, user_id, task):
        self.__check_is_valid_user(user_id)

        self.conn.execute(
            """
            INSERT INTO tasks(description, due_date, user_id, is_complete)
            VALUES ('{0}', DATETIME('{1}'), {2}, {3})
            """.format(task["description"], task["due_date"], user_id, 0))

        self.conn.commit()

    def update_task(self, task_id, task):
        self.__check_is_valid_task(task_id)

        attributes = [
            ("description", str),
            ("due_date", datetime),
            ("is_complete", bool),
        ]

        num_attributes_updated = 0

        for attribute, attr_type in attributes:
            if attribute in task:
                self.conn.execute(
                    """
                    UPDATE tasks
                    SET {0}={1}
                    WHERE ID={2}
                    """.format(attribute,
                               self.__get_sqlite_input(task[attribute], attr_type),
                               task_id))
                num_attributes_updated += 1

        if num_attributes_updated == 0:
            raise RuntimeError(
                "No valid attributes found. task_id: {0} task: {1}".format(
                    task_id, task))

        self.conn.commit()

    def __check_is_valid_user(self, user_id):
        cur = self.conn.execute("SELECT COUNT(*) FROM users WHERE ID = %s" % user_id)
        if int(cur.fetchone()["COUNT(*)"]) <= 0:
            raise RuntimeError("No user found for id: {0}".format(user_id))

    def __check_is_valid_task(self, task_id):
        cur = self.conn.execute("SELECT COUNT(*) FROM tasks WHERE ID = %s" % task_id)
        if int(cur.fetchone()["COUNT(*)"]) <= 0:
            raise RuntimeError("No task found for id: {0}".format(task_id))

    def __get_sqlite_input(self, attr, attr_type):
        if attr_type == str:
            return "'{0}'".format(attr)
        elif attr_type == datetime:
            return "DATETIME('{0}')".format(attr)
        elif attr_type == bool:
            return "{0}".format(int(attr))
        else:
            raise TypeError("Unknown attr_type: " + str(attr_type))


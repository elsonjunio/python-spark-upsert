import sqlite3
from datetime import datetime


def process_row(row, cur):
    now = datetime.now()

    id = row.__getitem__("id")
    name = row.__getitem__("name")
    note = row.__getitem__("note")

    sql_string = f""" INSERT INTO stocks(id,name,note) VALUES({id},'{name}','{note}')
                    ON CONFLICT(id) DO UPDATE SET name=excluded.name, note='{now.strftime("%Y-%m-%d %H:%M:%S")}';
                    """
    cur.execute(sql_string)


def process_partition(partition):

    database = "example.db"

    con = sqlite3.connect(database)

    cur = con.cursor()

    for row in partition:
        process_row(row, cur)

    con.commit()
    cur.close()
    con.close()

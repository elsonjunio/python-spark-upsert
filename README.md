# python-spark-upsert

This project was created to exemplify how to create UPSET operations using PySpark. To do this we can use pyspark.rdd.coalesce to reduce the number of partitions in a DataFrame.

To get these partitions we can use pyspark.rdd.foreachpartition, this method calls a callback function for each partition.

```python
df_csv.rdd.coalesce(10).foreachPartition(process_partition)
```
In a separate file, I put the code that will be called for the pyspark.rdd.foreachpartition method to make the SQL instructions and execute de UPSET.

```python
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
```



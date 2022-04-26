import sqlite3
con = sqlite3.connect('example.db')

cur = con.cursor()

# Create table
cur.execute('''CREATE TABLE stocks
               (id INTEGER NOT NULL PRIMARY KEY, name text, note text)''')

# Insert a row of data
cur.execute("INSERT INTO stocks VALUES (1,'elson','test a')")
cur.execute("INSERT INTO stocks VALUES (2,'duda','test b')")

# Save (commit) the changes
con.commit()

# We can also close the connection if we are done with it.
# Just be sure any changes have been committed or they will be lost.
con.close()

import psycopg2

connection = psycopg2.connect('dbname=demo')

cursor = connection.cursor()

cursor.execute(''' DROP TABLE IF EXISTS table1''')

cursor.execute('''
    CREATE TABLE table1(
        id INTEGER PRIMARY KEY,
        completed BOOLEAN NOT NULL DEFAULT FALSE
    );
''')

cursor.execute('INSERT INTO table1 (id, completed) VALUES (1, TRUE);')

SQL = 'INSERT INTO table1 (id, completed) VALUES (%(id)s, %(completed)s)'

data = {
    'id': 2,
    'completed': True
}

cursor.execute(SQL, data)

data = {
    'id': 3,
    'completed': False
}

cursor.execute(SQL, data)

''' fetching section '''

cursor.execute('select * from table1') # shows [(1, true), (2, true), (3, false)]

result1 = cursor.fetchmany(2) # result1 = first two rows from the query [(1, true), (2, ture)]
result2 = cursor.fetchone() # resul2 = the last one of the query
result3 = cursor.fetchone() # result3 = None since there is no query result left
print('first query: ')
print('fetchmany(2)', result1)
print('fetchone()', result2)
print('fetchone()', result3)

cursor.execute('select * from table1') # if we execute again, it generates a new quey
result4 = cursor.fetchall()
print('second qeury: ')
print('fetchall()', result4)

connection.commit()
cursor.close()
connection.close()

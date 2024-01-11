import sqlite3

conn = sqlite3.connect('products.sqlite')

c = conn.cursor()
c.execute('''
          CREATE TABLE products
          (id INTEGER PRIMARY KEY ASC, 
           name VARCHAR(100) NOT NULL,
           brand VARCHAR(100) NOT NULL,
           packaging VARCHAR(100) NOT NULL,
           price FLOAT NOT NULL,
           rating FLOAT NOT NULL,
           discount FLOAT,
           is_on_discount INTEGER NOT NULL,
           type VARCHAR(8) NOT NULL,
           shade VARCHAR(100),
           skin_type VARCHAR(100),
           skin_concern VARCHAR(100),
           waterproof INTEGER)
          ''')

conn.commit()
conn.close()

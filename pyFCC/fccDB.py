import sqlite3
from pyFCC.archive import parse_fcc_id

# creates a sqlite database for use with grantee data
def create_grantee_table():
    conn = sqlite3.connect('FCC.db')
    c = conn.cursor()

    c.execute("""DROP TABLE IF EXISTS grantees""")
    conn.commit()

    c.execute('''CREATE TABLE grantees
                (grantee_code int PRIMARY KEY NOT NULL,  
                grantee_name text,
                mailing_address text,
                po_box text,
                city text,
                state text,
                country text,
                zip_code text,
                contact_name text,
                date_received text)''')
    conn.commit()
    c.close()
    print("Grantee table created in FCC.db")

def create_product_table():
    conn = sqlite3.connect('FCC.db')
    c = conn.cursor()

    c.execute('''CREATE TABLE IF NOT EXISTS products
                (grantee_code int NOT NULL REFERENCES grantees(grantee_code),  
                product_code text,
                url text,
                high_freq text,
                low_freq text,
                version text,
                UNIQUE(grantee_code, product_code, version))''')
    conn.commit()
    c.close()
    print("Product table created in FCC.db")

# populates an existing database table with grantee data
def populate_grantees(grantee_test):
    conn = sqlite3.connect('FCC.db')
    c = conn.cursor()
    c.executemany('INSERT INTO grantees VALUES (?,?,?,?,?,?,?,?,?,?)', grantee_test)
    conn.commit()
    c.close()
    print("Grantee Table populated in FCC.db")

# populates an existing database table with product data
def populate_products(product_test):
    product_list = []
    for key, value in product_test.items():
            for row in value:
                dbValues = (row['grantee_code'], row['product_code'], row['url'], row['low_freq'], row['high_freq'], row['version'])
                product_list.append(dbValues)

    conn = sqlite3.connect('FCC.db')
    c = conn.cursor()
    c.executemany('INSERT OR IGNORE INTO products VALUES (?,?,?,?,?,?)', product_list)
    conn.commit()
    c.close()
    print("Product Table populated in FCC.db")


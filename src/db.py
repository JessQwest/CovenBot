import sqlite3

global conn, c

def connect_db():
    global conn, c
    # connect to the database
    conn = sqlite3.connect('sql.db')
    c = conn.cursor()
    print("Connected to database")
    create_tables()
    return conn, c

def create_tables():
    global conn, c
    if c is None:
        print("Database connection not established. Exiting...")
        return
    print("Creating tables if they do not exist")
    c.execute('''CREATE TABLE IF NOT EXISTS irl_groups (
        post_url text PRIMARY KEY NOT NULL,
        author text NOT NULL,
        coven_name text NOT NULL,
        region text NOT NULL,
        subregion text,
        min_age text,
        created_timestamp integer NOT NULL)''')


def fetch_records(table_name):
    global conn, c
    if c is None:
        print("Database connection not established. Exiting...")
        return
    c.execute(f"SELECT * FROM {table_name}")
    return c.fetchall()

def insert_irl_record(record):
    global conn, c
    if c is None:
        print("Database connection not established. Exiting...")
        return
    print(f"Insering record: {record}")
    c.execute("INSERT OR REPLACE INTO irl_groups (post_url, author, coven_name, region, subregion, min_age, created_timestamp) VALUES (?,?,?,?,?,?,?)", record)
    conn.commit()
    print(f"Record inserted: {record}")

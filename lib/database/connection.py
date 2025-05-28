import sqlite3

def get_connection():
    conn = sqlite3.connect('articles.db')
    conn.row_factory = sqlite3.Row  
    return conn

def set_database():
    with open("lib/database/schema.sql") as f:
        schema = f.read()
    conn = get_connection()
    conn.executescript(schema)
    conn.commit()
    conn.close()
    print("Database setup complete.")

if __name__ == "__main__":
    set_database()
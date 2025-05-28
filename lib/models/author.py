from lib.database.connection import get_connection

class Author:
    def __init__(self, id=None, name=None):
        self.id = id
        self.name = name
        if not name or not name.strip():
            raise ValueError("Author name cannot be empty")

    def save(self):
        conn = get_connection()
        cursor = conn.cursor()
        if self.id is None:
            cursor.execute("INSERT INTO authors (name) VALUES (?)", (self.name,))
            self.id = cursor.lastrowid
        else:
            cursor.execute("UPDATE authors SET name = ? WHERE id = ?", (self.name, self.id))
        conn.commit()
        conn.close()

    @classmethod
    def find_by_id(cls, author_id):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM authors WHERE id = ?", (author_id,))
        row = cursor.fetchone()
        conn.close()
        if row:
            return cls(id=row["id"], name=row["name"])
        return None

    @classmethod
    def find_by_name(cls, name):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM authors WHERE name = ?", (name,))
        row = cursor.fetchone()
        conn.close()
        if row:
            return cls(id=row["id"], name=row["name"])
        return None

    def articles(self):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM articles WHERE author_id = ?", (self.id,))
        articles = cursor.fetchall()
        conn.close()
        return articles

    def magazines(self):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT DISTINCT m.* FROM magazines m JOIN articles a ON m.id = a.magazine_id WHERE a.author_id = ?", (self.id,))
        magazines = cursor.fetchall()
        conn.close()
        return magazines

    def add_article(self, magazine, title):
        if not title or not title.strip():
            raise ValueError("Article title cannot be empty")
        if not magazine or not hasattr(magazine, "id"):
            raise ValueError("Magazine must be provided with an id")
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO articles (title, author_id, magazine_id) VALUES (?, ?, ?)", (title, self.id, magazine.id))
        conn.commit()
        conn.close()
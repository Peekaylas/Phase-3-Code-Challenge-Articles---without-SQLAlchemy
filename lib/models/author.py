from lib.database.connection import get_connection
from lib.models.article import Article

class Author:
    def __init__(self, name):
        self._id = None
        self._name = None
        self.name = name
        self.save()

    @property
    def id(self):
        return self._id

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, new_name):
        if hasattr(self, "_name") and self._name is not None:
            raise AttributeError("Name cannot be changed after being set")
        if not isinstance(new_name, str):
            raise TypeError("Name must be a string")
        if len(new_name) == 0:
            raise ValueError("Name must be longer than 0 characters")
        self._name = new_name
        if self._id is not None:
            self.save()

    def save(self):
        conn = get_connection()
        cursor = conn.cursor()
        if self._id is None:
            cursor.execute("INSERT INTO authors (name) VALUES (?)", (self._name,))
            self._id = cursor.lastrowid
        else:
            cursor.execute("UPDATE authors SET name = ? WHERE id = ?", (self._name, self._id))
        conn.commit()
        conn.close()

    @classmethod
    def find_by_id(cls, id):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT id, name FROM authors WHERE id = ?", (id,))
        row = cursor.fetchone()
        conn.close()
        if row:
            author = cls(row["name"])
            author._id = row["id"]
            return author
        return None

    def articles(self):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT id, title, author_id, magazine_id FROM articles WHERE author_id = ?", (self._id,))
        rows = cursor.fetchall()
        conn.close()
        return [Article.find_by_id(row["id"]) for row in rows]

    def magazines(self):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT DISTINCT m.id, m.name, m.category
            FROM magazines m
            JOIN articles a ON m.id = a.magazine_id
            WHERE a.author_id = ?
        """, (self._id,))
        rows = cursor.fetchall()
        conn.close()
        from lib.models.magazine import Magazine
        return [Magazine.find_by_id(row["id"]) for row in rows]

    def add_article(self, magazine, title):
        return Article(self, magazine, title)

    def topic_areas(self):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT DISTINCT m.category
            FROM magazines m
            JOIN articles a ON m.id = a.magazine_id
            WHERE a.author_id = ?
        """, (self._id,))
        rows = cursor.fetchall()
        conn.close()
        return [row["category"] for row in rows] if rows else None
from lib.database.connection import get_connection
from lib.models.article import Article

class Magazine:
    def __init__(self, name, category):
        self._id = None
        self._name = None
        self._category = None
        self.name = name
        self.category = category
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
        if not (2 <= len(new_name) <= 16):
            raise ValueError("Name must be between 2 and 16 characters long")
        self._name = new_name
        if self._id is not None:
            self.save()

    @property
    def category(self):
        return self._category

    @category.setter
    def category(self, new_category):
        if hasattr(self, "_category") and self._category is not None:
            raise AttributeError("Category cannot be changed after being set")
        if not isinstance(new_category, str):
            raise TypeError("Category must be a string")
        if len(new_category) == 0:
            raise ValueError("Category must have at least one character")
        self._category = new_category
        if self._id is not None:
            self.save()

    def save(self):
        conn = get_connection()
        cursor = conn.cursor()
        if self._id is None:
            cursor.execute("INSERT INTO magazines (name, category) VALUES (?, ?)", (self._name, self._category))
            self._id = cursor.lastrowid
        else:
            cursor.execute("UPDATE magazines SET name = ?, category = ? WHERE id = ?", (self._name, self._category, self._id))
        conn.commit()
        conn.close()

    @classmethod
    def find_by_id(cls, id):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT id, name, category FROM magazines WHERE id = ?", (id,))
        row = cursor.fetchone()
        conn.close()
        if row:
            magazine = cls(row["name"], row["category"])
            magazine._id = row["id"]
            return magazine
        return None

    def articles(self):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT id, title, author_id, magazine_id FROM articles WHERE magazine_id = ?", (self._id,))
        rows = cursor.fetchall()
        conn.close()
        return [Article.find_by_id(row["id"]) for row in rows]

    def contributors(self):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT DISTINCT a.id, a.name
            FROM authors a
            JOIN articles art ON a.id = art.author_id
            WHERE art.magazine_id = ?
        """, (self._id,))
        rows = cursor.fetchall()
        conn.close()
        from lib.models.author import Author
        return [Author.find_by_id(row["id"]) for row in rows]

    def article_titles(self):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT title FROM articles WHERE magazine_id = ?", (self._id,))
        rows = cursor.fetchall()
        conn.close()
        return [row["title"] for row in rows] if rows else None

    def contributing_authors(self):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT a.id, a.name
            FROM authors a
            JOIN articles art ON a.id = art.author_id
            WHERE art.magazine_id = ?
            GROUP BY a.id, a.name
            HAVING COUNT(art.id) >= 2
        """, (self._id,))
        rows = cursor.fetchall()
        conn.close()
        from lib.models.author import Author
        return [Author.find_by_id(row["id"]) for row in rows] if rows else None
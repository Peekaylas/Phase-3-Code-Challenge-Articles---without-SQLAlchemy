from lib.database.connection import get_connection
from lib.models.author import Author
from lib.models.magazine import Magazine

class Article:
    def __init__(self, author, magazine, title):
        self._id = None
        self._author = None
        self._magazine = None
        self._title = None
        self.author = author
        self.magazine = magazine
        self.title = title
        self.save()

    @property
    def id(self):
        return self._id

    @property
    def title(self):
        return self._title

    @title.setter
    def title(self, new_title):
        if hasattr(self, "_title") and self._title is not None:
            raise AttributeError("Title cannot be changed after being set")
        if not isinstance(new_title, str):
            raise TypeError("Title must be a string")
        if not (5 <= len(new_title) <= 50):
            raise ValueError("Title must be between 5 and 50 characters")
        self._title = new_title
        if self._id is not None:
            self.save()

    @property
    def author(self):
        return self._author

    @author.setter
    def author(self, new_author):
        if not isinstance(new_author, Author):
            raise TypeError("Author must be an instance of Author")
        self._author = new_author
        if self._id is not None:
            self.save()

    @property
    def magazine(self):
        return self._magazine

    @magazine.setter
    def magazine(self, new_magazine):
        if not isinstance(new_magazine, Magazine):
            raise TypeError("Magazine must be an instance of Magazine")
        self._magazine = new_magazine
        if self._id is not None:
            self.save()

    def save(self):
        conn = get_connection()
        cursor = conn.cursor()
        if self._id is None:
            cursor.execute(
                "INSERT INTO articles (title, author_id, magazine_id) VALUES (?, ?, ?)",
                (self._title, self._author.id, self._magazine.id)
            )
            self._id = cursor.lastrowid
        else:
            cursor.execute(
                "UPDATE articles SET title = ?, author_id = ?, magazine_id = ? WHERE id = ?",
                (self._title, self._author.id, self._magazine.id, self._id)
            )
        conn.commit()
        conn.close()

    @classmethod
    def find_by_id(cls, id):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT id, title, author_id, magazine_id FROM articles WHERE id = ?", (id,))
        row = cursor.fetchone()
        conn.close()
        if row:
            author = Author.find_by_id(row["author_id"])
            magazine = Magazine.find_by_id(row["magazine_id"])
            article = cls(author, magazine, row["title"])
            article._id = row["id"]
            return article
        return None
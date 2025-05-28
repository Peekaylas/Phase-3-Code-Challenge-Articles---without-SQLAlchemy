import pytest
from lib.models.article import Article
from lib.models.author import Author
from lib.models.magazine import Magazine
from lib.database.connection import get_connection

@pytest.fixture(autouse=True)
def setup_and_teardown():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.executescript("""
        CREATE TABLE IF NOT EXISTS authors (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL
        );
        CREATE TABLE IF NOT EXISTS magazines (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            category TEXT NOT NULL
        );
        CREATE TABLE IF NOT EXISTS articles (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            author_id INTEGER NOT NULL,
            magazine_id INTEGER NOT NULL,
            FOREIGN KEY (author_id) REFERENCES authors(id) ON DELETE CASCADE,
            FOREIGN KEY (magazine_id) REFERENCES magazines(id) ON DELETE CASCADE
        );
    """)
    cursor.execute("DELETE FROM articles")
    cursor.execute("DELETE FROM authors")
    cursor.execute("DELETE FROM magazines")
    conn.commit()
    conn.close()
    yield

def test_save_and_find_by_id():
    author = Author(name="Author1")
    author.save()
    magazine = Magazine(name="Mag1", category="Test")
    magazine.save()
    article = Article(title="Test Article", author_id=author.id, magazine_id=magazine.id)
    article.save()
    assert article.id is not None
    found = Article.find_by_id(article.id)
    assert found is not None
    assert found.title == "Test Article"
    assert found.author_id == author.id
    assert found.magazine_id == magazine.id

def test_find_by_title():
    author = Author(name="Author1")
    author.save()
    mag1 = Magazine(name="Mag1", category="Test1")
    mag2 = Magazine(name="Mag2", category="Test2")
    mag1.save()
    mag2.save()
    article1 = Article(title="Unique Title", author_id=author.id, magazine_id=mag1.id)
    article2 = Article(title="Unique Title", author_id=author.id, magazine_id=mag2.id)
    article1.save()
    article2.save()
    results = Article.find_by_title("Unique Title")
    assert len(results) == 2
    titles = [a.title for a in results]
    assert all(t == "Unique Title" for t in titles)

def test_find_by_author():
    author1 = Author(name="Author1")
    author2 = Author(name="Author2")
    author1.save()
    author2.save()
    magazine = Magazine(name="Mag1", category="Test")
    magazine.save()
    article1 = Article(title="Authored Article 1", author_id=author1.id, magazine_id=magazine.id)
    article2 = Article(title="Authored Article 2", author_id=author1.id, magazine_id=magazine.id)
    article3 = Article(title="Other Article", author_id=author2.id, magazine_id=magazine.id)
    article1.save()
    article2.save()
    article3.save()
    results = Article.find_by_author(author1.id)
    assert len(results) == 2
    for article in results:
        assert article.author_id == author1.id

def test_find_by_magazine():
    author = Author(name="Author1")
    author.save()
    mag1 = Magazine(name="Mag1", category="Test1")
    mag2 = Magazine(name="Mag2", category="Test2")
    mag1.save()
    mag2.save()
    article1 = Article(title="Mag 1 Article 1", author_id=author.id, magazine_id=mag1.id)
    article2 = Article(title="Mag 1 Article 2", author_id=author.id, magazine_id=mag1.id)
    article3 = Article(title="Mag 2 Article", author_id=author.id, magazine_id=mag2.id)
    article1.save()
    article2.save()
    article3.save()
    results = Article.find_by_magazine(mag1.id)
    assert len(results) == 2
    for article in results:
        assert article.magazine_id == mag1.id
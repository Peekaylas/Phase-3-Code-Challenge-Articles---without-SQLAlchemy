import pytest
from lib.models.author import Author
from lib.models.magazine import Magazine
from lib.database.connection import get_connection

@pytest.fixture(autouse=True)
def setup_and_teardown_db():
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

def test_create_and_find_author():
    author = Author(name="Test Author")
    author.save()
    assert author.id is not None
    found = Author.find_by_id(author.id)
    assert found is not None
    assert found.name == "Test Author"
    found_by_name = Author.find_by_name("Test Author")
    assert found_by_name is not None
    assert found_by_name.id == author.id

def test_articles_and_magazines_relationship():
    author = Author(name="Author1")
    author.save()
    magazine = Magazine(name="Magazine1", category="Tech")
    magazine.save()
    author.add_article(magazine, "Article1")
    articles = author.articles()
    assert len(articles) == 1
    assert articles[0]["title"] == "Article1"
    magazines = author.magazines()
    assert len(magazines) == 1
    assert magazines[0]["name"] == "Magazine1"

def test_add_article_method():
    author = Author(name="Author2")
    author.save()
    magazine = Magazine(name="Magazine2", category="Science")
    magazine.save()
    author.add_article(magazine, "New Article")
    articles = author.articles()
    assert any(a["title"] == "New Article" for a in articles)
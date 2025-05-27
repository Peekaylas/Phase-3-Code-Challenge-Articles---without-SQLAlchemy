import pytest
from lib.models.author import Author
from lib.models.magazine import Magazine
from lib.models.article import Article
from lib.database.connection import get_connection

@pytest.fixture
def setup_db():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.executescript(open("lib/database/schema.sql").read())  
    conn.commit()
    yield
    cursor.execute("DELETE FROM articles")
    cursor.execute("DELETE FROM magazines")
    cursor.execute("DELETE FROM authors")
    conn.commit()
    conn.close()

@pytest.fixture
def setup_author(setup_db):
    author = Author("John Doe")
    yield author

def test_author_creation(setup_author):
    author = setup_author
    assert author.name == "John Doe"

def test_author_name_immutable(setup_author):
    author = setup_author
    with pytest.raises(AttributeError):
        author.name = "Jane Doe"

def test_author_articles(setup_author):
    author = setup_author
    magazine = Magazine("Tech Weekly", "Technology")
    author.add_article(magazine, "Tech Trends 2025")
    articles = author.articles()
    assert len(articles) == 1
    assert articles[0].title == "Tech Trends 2025"
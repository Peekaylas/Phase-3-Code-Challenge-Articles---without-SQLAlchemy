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

def test_article_creation(setup_db):
    author = Author("John Doe")
    magazine = Magazine("Tech Weekly", "Technology")
    article = Article(author, magazine, "Tech Trends 2025")
    assert article.title == "Tech Trends 2025"
    assert article.author.name == "John Doe"
    assert article.magazine.name == "Tech Weekly"

def test_article_title_immutable(setup_db):
    author = Author("John Doe")
    magazine = Magazine("Tech Weekly", "Technology")
    article = Article(author, magazine, "Tech Trends 2025")
    with pytest.raises(AttributeError):
        article.title = "New Title"

def test_article_title_validation(setup_db):
    author = Author("John Doe")
    magazine = Magazine("Tech Weekly", "Technology")
    with pytest.raises(ValueError):
        Article(author, magazine, "Shrt")  
    with pytest.raises(ValueError):
        Article(author, magazine, "A" * 51)  
    with pytest.raises(TypeError):
        Article(author, magazine, 123)  
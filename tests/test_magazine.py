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
def setup_magazine(setup_db):
    magazine = Magazine("Tech Weekly", "Technology")
    yield magazine

def test_magazine_creation(setup_magazine):
    magazine = setup_magazine
    assert magazine.name == "Tech Weekly"
    assert magazine.category == "Technology"

def test_magazine_name_immutable(setup_magazine):
    magazine = setup_magazine
    with pytest.raises(AttributeError):
        magazine.name = "New Magazine"

def test_magazine_contributors(setup_magazine):
    magazine = setup_magazine
    author1 = Author("John Doe")
    author2 = Author("Jane Smith")
    author1.add_article(magazine, "Tech Trends 2025")
    author2.add_article(magazine, "AI Revolution")
    contributors = magazine.contributors()
    assert len(contributors) == 2
    assert contributors[0].name in ["John Doe", "Jane Smith"]
    assert contributors[1].name in ["John Doe", "Jane Smith"]
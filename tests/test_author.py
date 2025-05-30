import pytest
from lib.models.author import Author
from lib.database.connection import get_connection

@pytest.fixture(autouse=True)
def setup_and_teardown_db():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM articles")
    cursor.execute("DELETE FROM authors")
    conn.commit()
    conn.close()
    yield
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM articles")
    cursor.execute("DELETE FROM authors")
    conn.commit()
    conn.close()

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
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO authors (name) VALUES (?)", ("Author1",))
    author_id = cursor.lastrowid

    cursor.execute("INSERT INTO magazines (name, category) VALUES (?, ?)", ("Magazine1", "Tech"))
    magazine_id = cursor.lastrowid

    cursor.execute("INSERT INTO articles (title, author_id, magazine_id) VALUES (?, ?, ?)", ("Article1", author_id, magazine_id))
    conn.commit()
    conn.close()

    author = Author.find_by_id(author_id)
    articles = author.articles()
    assert len(articles) == 1
    assert articles[0]["title"] == "Article1"

    magazines = author.magazines()
    assert len(magazines) == 1
    assert magazines[0]["name"] == "Magazine1"

def test_add_article_method():
    from lib.models.magazine import Magazine  
    author = Author(name="Author2")
    author.save()

    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO magazines (name, category) VALUES (?, ?)", ("Magazine2", "Science"))
    magazine_id = cursor.lastrowid
    conn.commit()
    conn.close()

    class DummyMagazine:
        def __init__(self, id):
            self.id = id

    mag = DummyMagazine(magazine_id)

    author.add_article(mag, "New Article")
    articles = author.articles()
    assert any(a["title"] == "New Article" for a in articles)
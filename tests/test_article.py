import pytest
from lib.models.article import Article
from lib.database.connection import get_connection

@pytest.fixture(autouse=True)
def setup_and_teardown():
    # Clear articles table before each test
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM articles")
    conn.commit()
    conn.close()
    yield
    # You can add teardown code here if needed

def test_save_and_find_by_id():
    article = Article(title="Test Article", author_id=1, magazine_id=1)
    article.save()
    assert article.id is not None

    found = Article.find_by_id(article.id)
    assert found is not None
    assert found.title == "Test Article"
    assert found.author_id == 1
    assert found.magazine_id == 1

def test_find_by_title():
    article1 = Article(title="Unique Title", author_id=1, magazine_id=1)
    article2 = Article(title="Unique Title", author_id=2, magazine_id=2)
    article1.save()
    article2.save()

    results = Article.find_by_title("Unique Title")
    assert len(results) >= 2
    titles = [a.title for a in results]
    assert all(t == "Unique Title" for t in titles)

def test_find_by_author():
    article1 = Article(title="Authored Article 1", author_id=5, magazine_id=1)
    article2 = Article(title="Authored Article 2", author_id=5, magazine_id=2)
    article3 = Article(title="Other Article", author_id=6, magazine_id=1)
    article1.save()
    article2.save()
    article3.save()

    results = Article.find_by_author(5)
    assert len(results) == 2
    for article in results:
        assert article.author_id == 5

def test_find_by_magazine():
    article1 = Article(title="Mag 1 Article 1", author_id=1, magazine_id=10)
    article2 = Article(title="Mag 1 Article 2", author_id=2, magazine_id=10)
    article3 = Article(title="Mag 2 Article", author_id=3, magazine_id=11)
    article1.save()
    article2.save()
    article3.save()

    results = Article.find_by_magazine(10)
    assert len(results) == 2
    for article in results:
        assert article.magazine_id == 10
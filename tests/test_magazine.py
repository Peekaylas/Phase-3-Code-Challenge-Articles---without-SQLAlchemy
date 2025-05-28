import pytest
from lib.models.magazine import Magazine
from lib.database.connection import get_connection

@pytest.fixture(autouse=True)
def setup_and_teardown():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.executescript("""
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
            FOREIGN KEY (magazine_id) REFERENCES magazines(id) ON DELETE CASCADE
        );
    """)
    cursor.execute("DELETE FROM magazines")
    cursor.execute("DELETE FROM articles")
    conn.commit()
    conn.close()
    yield

def test_save_and_find_by_id():
    mag = Magazine(name="Tech Monthly", category="Technology")
    mag.save()
    assert mag.id is not None
    found = Magazine.find_by_id(mag.id)
    assert found is not None
    assert found.name == "Tech Monthly"
    assert found.category == "Technology"

def test_find_by_name():
    mag = Magazine(name="Health Weekly", category="Health")
    mag.save()
    found = Magazine.find_by_name("Health Weekly")
    assert found is not None
    assert found.category == "Health"

def test_find_by_category():
    mag1 = Magazine(name="Science Daily", category="Science")
    mag2 = Magazine(name="Science Weekly", category="Science")
    mag1.save()
    mag2.save()
    results = Magazine.find_by_category("Science")
    assert len(results) == 2
    names = [m.name for m in results]
    assert "Science Daily" in names and "Science Weekly" in names

def test_article_titles_empty():
    mag = Magazine(name="Empty Mag", category="Misc")
    mag.save()
    assert mag.article_titles() == []
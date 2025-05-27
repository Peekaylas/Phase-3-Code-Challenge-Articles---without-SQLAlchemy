import pytest
from lib.models.author import Author
from lib.models.magazine import Magazine
from lib.models.article import Article

@pytest.fixture
def setup_magazine():
    Article.all = []  
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
    assert len(magazine.contributors()) == 2
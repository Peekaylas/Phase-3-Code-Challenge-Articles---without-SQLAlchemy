import pytest
from lib.models.author import Author
from lib.models.magazine import Magazine
from lib.models.article import Article

@pytest.fixture
def setup_article():
    Article.all = []  
    author = Author("John Doe")
    magazine = Magazine("Tech Weekly", "Technology")
    article = Article(author, magazine, "Tech Trends 2025")
    yield article

def test_article_creation(setup_article):
    article = setup_article
    assert article.title == "Tech Trends 2025"
    assert article.author.name == "John Doe"
    assert article.magazine.name == "Tech Weekly"

def test_article_title_immutable(setup_article):
    article = setup_article
    with pytest.raises(AttributeError):
        article.title = "New Title"

def test_article_title_validation():
    author = Author("John Doe")
    magazine = Magazine("Tech Weekly", "Technology")
    with pytest.raises(ValueError):
        Article(author, magazine, "Shrt")  
    with pytest.raises(ValueError):
        Article(author, magazine, "A" * 51)  
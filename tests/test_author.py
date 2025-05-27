import pytest
from lib.models.author import Author
from lib.models.magazine import Magazine
from lib.models.article import Article

@pytest.fixture
def setup_author():
    Article.all = []  
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
    assert len(author.articles()) == 1
    assert author.articles()[0].title == "Tech Trends 2025"
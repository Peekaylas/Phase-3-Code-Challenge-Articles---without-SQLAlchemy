class Magazine:
    def __init__(self b
    self._name = None
        self._category = None
        self.name = name
        self.category = category

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, new_name):
        if hasattr(self, "_name") and self._name is not None:
            raise AttributeError("Name cannot be changed after being set")
        if not isinstance(new_name, str):
            raise TypeError("Name must be a string")
        if not (2 <= len(new_name) <= 16):
            raise ValueError("Name must be between 2 and 16 characters long")
        self._name = new_name

    @property
    def category(self):
        return self._category

    @category.setter
    def category(self, new_category):
        if hasattr(self, "_category") and self._category is not None:
            raise AttributeError("Category cannot be changed after being set")
        if not isinstance(new_category, str):
            raise TypeError("Category must be a string")
        if len(new_category) == 0:
            raise ValueError("Category must have at least one character")
        self._category = new_category

    def articles(self):
        from lib.models.article import Article
        return [article for article in Article.all if article.magazine == self]

    def contributors(self):
        return list({article.author for article in self.articles()})

    def article_titles(self):
        article_titles = [article.title for article in self.articles()]
        return article_titles if article_titles else None

    def contributing_authors(self):
        authors = {}
        for article in self.articles():
            authors[article.author] = authors.get(article.author, 0) + 1
        contributing_authors = [author for author, count in authors.items() if count >= 2]
        return contributing_authors if contributing_authors else None
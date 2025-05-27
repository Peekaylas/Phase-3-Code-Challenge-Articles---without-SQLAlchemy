class Author:
    def __init__(self, name):
        self._name = None
        self.name = name

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, new_name):
        if hasattr(self, "_name") and self._name is not None:
            raise AttributeError("Name cannot be changed after being set")
        if not isinstance(new_name, str):
            raise TypeError("Name must be a string")
        if len(new_name) == 0:
            raise ValueError("Name must be longer than 0 characters")
        self._name = new_name

    def articles(self):
        from lib.models.article import Article
        return [article for article in Article.all if article.author == self]

    def magazines(self):
        return list({article.magazine for article in self.articles()})

    def add_article(self, magazine, title):
        from lib.models.article import Article
        return Article(self, magazine, title)

    def topic_areas(self):
        topic_areas = list({magazine.category for magazine in self.magazines()})
        return topic_areas if topic_areas else None
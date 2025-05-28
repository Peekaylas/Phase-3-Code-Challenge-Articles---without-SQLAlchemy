def author(self):
    from lib.models.author import Author
    return Author.find_by_id(self.author_id)

def magazine(self):
    from lib.models.magazine import Magazine
    return Magazine.find_by_id(self.magazine_id)
from lib.models.author import Author
from lib.models.magazine import Magazine
from lib.models.article import Article

def run_examples():
    Article.all = []  

    author1 = Author("John Doe")
    author2 = Author("Jane Smith")
    magazine1 = Magazine("Tech Weekly", "Technology")
    magazine2 = Magazine("Fashion Daily", "Fashion")

    author1.add_article(magazine1, "Tech Trends 2025")
    author1.add_article(magazine1, "AI Revolution")
    author2.add_article(magazine1, "Future Tech")
    author2.add_article(magazine2, "Fashion Forward")

    print(f"Articles by {author1.name}:")
    for article in author1.articles():
        print(f"- {article.title}")

    print(f"\nMagazines {author1.name} contributed to:")
    for magazine in author1.magazines():
        print(f"- {magazine.name} ({magazine.category})")

    print(f"\nArticles in {magazine1.name}:")
    for title in magazine1.article_titles() or []:
        print(f"- {title}")

    print(f"\nContributing authors to {magazine1.name}:")
    for author in magazine1.contributing_authors() or []:
        print(f"- {author.name}")

if __name__ == "__main__":
    run_examples()
from myadmin.models import Category, Article
from .define import *

def sidebar(request):
    categories = Category.objects.all()
    recent_articles = Article.objects.all().order_by('-publish_date')[:NEWS_RECENT_ARTICLE_NUMBER]
    return {
        'categories': categories,
        'recent_articles': recent_articles,
    }

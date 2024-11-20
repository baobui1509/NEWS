from django.shortcuts import render, redirect
from myadmin.models import Article, Category
from .define import *
from django.core.paginator import Paginator
from django.db.models import Q
from myadmin.forms import *


def home_index(request):
    special_articles = Article.objects.filter(is_homepage=True, special=True).order_by('-publish_date')[:NEWS_HOMEPAGE_SPECIAL_ARTICLES_NUMBER]
    categories = Category.objects.all()
    latest_articles = Article.objects.filter(is_homepage=True, category__layout='grid').order_by('-publish_date')[:NEWS_LATEST_ARTICLE_NUMBER]
    featured_latest_article = latest_articles[0] if latest_articles else None
    other_latest_articles = latest_articles[1:] if latest_articles.count() > 1 else None
    featured_categories = Category.objects.filter(is_homepage=True)
    homepage_articles_grid = Article.objects.filter(category__layout='grid', category__is_homepage=True)[:NEWS_HOMEPAGE_GRID_ARTICLES_NUMBER]
    homepage_articles_list = Article.objects.filter(category__layout='list', category__is_homepage=True)[:NEWS_HOMEPAGE_LIST_ARTICLES_NUMBER]

    return render(request, 'news/pages/home/index.html', {
        'special_articles': special_articles,
        'categories': categories,
        'featured_latest_article': featured_latest_article,
        'other_latest_articles': other_latest_articles,
        'featured_categories': featured_categories,
        'homepage_articles_grid': homepage_articles_grid,
        'homepage_articles_list': homepage_articles_list,
    })
    
def category_index(request, slug):
    items = Article.objects.filter(category__slug=slug)
    paginator = Paginator(items, NEWS_CATEGORY_PAGINATION_NUMBER)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'news/pages/category/index.html', {
       'items': items,
       'page_obj': page_obj
    })
    
    
def search(request):
    # categories = Category.objects.all()
    # recent_articles = Article.objects.all().order_by('-publish_date')[:NEWS_RECENT_ARTICLE_NUMBER]
    keyword = request.GET.get('keyword', '')
    items = []

    if keyword:
        items = Article.objects.filter(
            Q(name__icontains=keyword) | Q(content__icontains=keyword)
        ).order_by('-publish_date')
    paginator = Paginator(items, NEWS_CATEGORY_PAGINATION_NUMBER)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'news/pages/article/search.html', {
        'keyword': keyword,
        'items': items,
        'page_obj': page_obj,
        # 'categories': categories,
        # 'recent_articles': recent_articles,
    }   
    )
    
def article_index(request, slug):
    item = Article.objects.filter(slug=slug).first()
    return render(request, 'news/pages/article/index.html', {
        'item': item,
    }   
    )
    
def contact_index(request):
    return render(request, 'news/pages/contact/index.html', {
    })
    
def contact_view(request):
    success_message = ''
    error_message = ''
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            request.session['success_message'] = 'Gửi lời nhắn thành công!'
            
        else:
            request.session['error_message'] = form.errors
        success_message = request.session.pop('success_message', None)
        error_message = request.session.pop('error_message', None)
        return redirect('contact_index_news')  
    else:
        form = ContactForm()
    
    print('success_message:' ,success_message)

    print('error_message:' ,error_message)
    return render(request, 'news/pages/contact/index.html', {
        'form': form,
        'success_message': success_message,
        'error_message': error_message,
        })
    
def tag_index(request, slug):
    items = Article.objects.filter(tags__slug=slug)
    for item in items:
        print('article: ', item.name)
        print('tag: ', item.tags.name)
    paginator = Paginator(items, NEWS_CATEGORY_PAGINATION_NUMBER)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'news/pages/tag/index.html', {
       'items': items,
       'page_obj': page_obj
    })

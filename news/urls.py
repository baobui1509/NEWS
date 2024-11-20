from django.urls import path
from . import views

urlpatterns = [
    path("", views.home_index, name="home_index"),
    path("category/<slug:slug>/", views.category_index, name="category_index"),
    path("tag/<slug:slug>/", views.tag_index, name="tag_index"),
    path('search/', views.search, name='search'),
    path('contact/', views.contact_index, name='contact_index_news'),    
    path('contact/view/', views.contact_view, name='contact_view'),    
    path('article/<slug:slug>/', views.article_index, name='article_index'),
    # path('category/', views.category_index, name='category_index'),
    # path('category/create', views.category_create, name='category_create'),
    # path('category/edit/<int:id>', views.category_edit, name='category_edit'),
    # path('delete/<str:item_type>/<int:id>/', views.item_delete, name='item_delete'),
    # path('bulk-delete/<str:item_type>', views.bulk_delete, name='bulk_delete'),
    #
    # path('article/', views.article_index, name='article_index'),
    # path('article/create', views.article_create, name='article_create'),
    # path('article/edit/<int:id>', views.article_edit, name='article_edit'),
]

# https://hungphuquoc.vn/admin/login
# https://themegenix.net/html/zaira/index.html
# https://html.themewant.com/echo/


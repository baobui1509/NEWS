from django.urls import path
from . import views

urlpatterns = [
    path("", views.home_index, name="home_index"),
    
    path('get-tags/', views.get_tags, name='get_tags'),
    
    path('category/', views.category_index, name='category_index'),
    path('category/create', views.category_create, name='category_create'),
    path('category/edit/<int:id>', views.category_edit, name='category_edit'),
    
    path('delete/<str:item_type>/<int:id>/', views.item_delete, name='item_delete'),
    path('bulk-delete/<str:item_type>', views.bulk_delete, name='bulk_delete'),

    path('article/', views.article_index, name='article_index'),
    path('article/create', views.article_create, name='article_create'),
    path('article/edit/<int:id>', views.article_edit, name='article_edit'),
    
    path('contact/', views.contact_index, name='contact_index_myadmin'),
    path('contact/edit/<int:id>', views.contact_edit, name='contact_myadmin_edit'),
    
    path('tag/', views.tag_index, name='tag_index'),
    path('tag/create', views.tag_create, name='tag_create'),
    path('tag/edit/<int:id>', views.tag_edit, name='tag_edit'),
    
    
    # path('article/delete/<int:id>/', views.article_delete, name='article_delete'),
    # path('category/filter', views.filter_items, name='filter_items'),
]

# https://hungphuquoc.vn/admin/login
# https://themegenix.net/html/zaira/index.html
# https://html.themewant.com/echo/


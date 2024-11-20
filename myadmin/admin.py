from django.contrib import admin

from myadmin.models import Category, Article, Contact, Tag

class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ["name"]}

class ArticleAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ["name"]}
    
class ContactAdmin(admin.ModelAdmin):
    pass

class TagAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ["name"]}

admin.site.register(Category, CategoryAdmin)
admin.site.register(Article, ArticleAdmin)
admin.site.register(Contact, ContactAdmin)
admin.site.register(Tag, TagAdmin)

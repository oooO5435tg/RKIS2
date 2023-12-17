from django.contrib import admin

from .models import Author, Book, Cover, Category, Genre

admin.site.register(Author)
admin.site.register(Book)
admin.site.register(Cover)
admin.site.register(Category)
admin.site.register(Genre)

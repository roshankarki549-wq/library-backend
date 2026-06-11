from django.contrib import admin

from library.library.books.models import Book
from members.models import Member
from django.contrib import admin
from .models import Book

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'author',
        'category',
        'isbn',
        'total_copies',
        'available_copies',
        'created_at',
    )
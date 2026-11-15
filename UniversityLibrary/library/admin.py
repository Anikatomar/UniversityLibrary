
from django.contrib import admin
from .models import Author, Book, Student, BorrowRecord


# Author Admin
@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'country')


# Book Admin
@admin.register(Book)
class BookAdmin(admin.ModelAdmin):

    list_display = ('title', 'isbn', 'author', 'price', 'published_year')

    search_fields = ('title', 'isbn')

    list_filter = ('author',)

    ordering = ('price',)


# Student Admin
@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('name', 'roll_no', 'email', 'branch')


# BorrowRecord Admin
@admin.register(BorrowRecord)
class BorrowRecordAdmin(admin.ModelAdmin):

    list_display = ('student', 'book', 'borrow_date', 'return_date', 'status')

    search_fields = ('student__name', 'book__title')

    list_filter = ('status',)

    ordering = ('borrow_date',)

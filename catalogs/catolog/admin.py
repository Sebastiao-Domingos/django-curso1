from django.contrib import admin
from . models import *


# Register your models here.


class BookInstanceLine(admin.TabularInline):
    model = Book

class AuthorInstanceLine(admin.TabularInline):
    model = Author


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ("name", "date_of_birth", "date_of_death")


@admin.register(BookInstance)
class BookInstanceAdmin(admin.ModelAdmin):
    list_display = ('books', 'status', 'borrower', 'due_back', 'id')
    list_filter = ('status', 'due_back')

    fieldsets = (
        (None, {
            'fields': ('books','imprint', 'id')
        }),
        ('Availability', {
            'fields': ('status', 'due_back','borrower')
        }),
    )


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ("title", "summary", "ISBN", "language")





@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ("id", "name" , "created_at", "updated_at")
    list_filter = ["name"]

@admin.register(Language)
class LanguageAdmin(admin.ModelAdmin):
    list_display = ("id", "name" , "created_at", "updated_at")
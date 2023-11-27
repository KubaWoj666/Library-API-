from django.contrib import admin

from .models import Author, Book, Review




class AuthorAdmin(admin.ModelAdmin):
    list_display = ["name", "last_name"]

class ReviewAdmin(admin.ModelAdmin):
    list_display = ["book", "owner", "rating"]



admin.site.register(Author, AuthorAdmin)
admin.site.register(Book)
admin.site.register(Review, ReviewAdmin)
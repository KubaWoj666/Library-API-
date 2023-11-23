from django.urls import path
from . import views

urlpatterns = [
    path("authors/", views.AuthorListCreateAPIView.as_view(), name="authors-list"),
    path("authors/<int:pk>/", views.AuthorDetailAPIView.as_view(), name="author-detail"),

    path("books/", views.BookListCreateAPIView.as_view(), name="books-list"),
    path("books/<int:pk>/", views.BookDetailAPIView.as_view(), name="book-detail")


]
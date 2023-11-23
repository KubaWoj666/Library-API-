from rest_framework import generics

from books.models import Author, Book
from .serializer import AuthorSerializer, AuthorCreateSerializer, AuthorDetailSerializer, BookSerializer, BookDetailSerializer, BookCreateSerializer



class AuthorListCreateAPIView(generics.ListCreateAPIView):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer

    def get_serializer_class(self):
        if self.request.method == "GET":
            return AuthorSerializer
        elif self.request.method == "POST":
            return AuthorCreateSerializer

class AuthorDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Author.objects.all()
    serializer_class = AuthorDetailSerializer


class BookListCreateAPIView(generics.ListCreateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

    def get_serializer_class(self):
        if self.request.method == "GET":
            return BookSerializer
        elif self.request.method == "POST":
            return BookCreateSerializer


class BookDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Book.objects.all()
    serializer_class = BookDetailSerializer
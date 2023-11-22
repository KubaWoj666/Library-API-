from rest_framework import generics

from books.models import Author, Book
from .serializer import AuthorSerializer, AuthorDetailSerializer, BookSerializer



class AuthorListCreateAPIView(generics.ListCreateAPIView):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer


class AuthorDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Author.objects.all()
    serializer_class = AuthorDetailSerializer


from rest_framework import generics
from rest_framework.exceptions import ValidationError
from rest_framework.generics import get_object_or_404


from books.models import Author, Book, Review
from .serializer import (AuthorSerializer, AuthorCreateSerializer, AuthorDetailSerializer, 
                        BookSerializer, BookDetailSerializer, BookCreateSerializer,
                        ReviewSerializer)



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



class ReviewCreateAPIView(generics.CreateAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer

    def perform_create(self, serializer):
        book_id = self.kwargs.get("pk")

        book_obj = get_object_or_404(Book, id=book_id)

        owner = serializer.validated_data.get("owner")

        if Review.objects.filter(book=book_obj, owner=owner).exists():
            raise ValidationError("You have already review this book")
        
        serializer.save(book=book_obj, owner=owner)

        return super().perform_create(serializer)


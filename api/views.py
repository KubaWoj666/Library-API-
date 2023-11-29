from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from rest_framework.generics import get_object_or_404


from books.models import Author, Book, Review
from .pagination import ReviewPagination
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


class ReviewListForBook(generics.ListAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    pagination_class = ReviewPagination
    

    def get_queryset(self):
        book_id  = self.kwargs.get("pk")
        try:
            book_obj = Book.objects.get(id=book_id)
        except Book.DoesNotExist:
            return Review.objects.none()


        reviews = Review.objects.filter(book=book_obj)

        return reviews
    
    def list(self, request, *args, **kwargs):
        book_id = self.kwargs.get("pk")
        reviews = self.get_queryset()
         
        paginated_reviews = self.paginate_queryset(reviews)
        serializer = self.get_serializer(paginated_reviews, many=True)  
        

        try:
            book_obj = Book.objects.get(id=book_id)
        except:
            response = {
                "message": "Book does not exist!"
            }
            return Response(data=response, status=status.HTTP_404_NOT_FOUND)


        if not reviews.exists():
            response = {
                "message": f"Book '{book_obj.title}' have no reviews."
            }

            return Response(data=response, status=status.HTTP_200_OK)
        
        response = {
            "message" : f"Reviews for '{book_obj.title}'. ",
            "data": serializer.data
        }

        if paginated_reviews is not None:
            response.update({
                "count": self.paginator.page.paginator.count,
                "next": self.paginator.get_next_link(),
                "previous": self.paginator.get_previous_link()
            })
        
        return Response(data=response, status=status.HTTP_200_OK)
        

class ReviewDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer

 
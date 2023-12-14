from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated, AllowAny

from books.models import Author, Book, Review
from accounts.models import User

from .pagination import ReviewPagination
from .permissions import OwnerOrReadOnly, AdminOrReadOnly
from .serializer import (AuthorSerializer, AuthorCreateSerializer, AuthorDetailSerializer, 
                        BookSerializer, BookDetailSerializer, BookCreateSerializer,
                        ReviewSerializer, UserReviewsSerializer,
                        MyTokenObtainPairSerializer, RegisterUserSerializer, ChangePasswordSerializer, UpdateUserProfileSerializer, UserSerializer)

from rest_framework_simplejwt.views import TokenObtainPairView



class AuthorListCreateAPIView(generics.ListCreateAPIView):
    queryset = Author.objects.all().order_by("id")
    serializer_class = AuthorSerializer
    permission_classes = [IsAuthenticated, AdminOrReadOnly]
    pagination_class = ReviewPagination

    def get_serializer_class(self):
        if self.request.method == "GET":
            return AuthorSerializer
        elif self.request.method == "POST":
            return AuthorCreateSerializer

class AuthorDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Author.objects.all()
    serializer_class = AuthorDetailSerializer
    permission_classes = [IsAuthenticated, AdminOrReadOnly]


"""BOOKS VIEWS"""

class BookListCreateAPIView(generics.ListCreateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated, AdminOrReadOnly]
    pagination_class = ReviewPagination

    def get_serializer_class(self):
        if self.request.method == "GET":
            return BookSerializer
        elif self.request.method == "POST":
            return BookCreateSerializer


class BookDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Book.objects.all()
    serializer_class = BookDetailSerializer
    permission_classes = [IsAuthenticated, AdminOrReadOnly]
    

"""REVIEW VIEWS"""

class UserReviewAPIView(generics.ListAPIView):
    queryset = Review.objects.all()
    serializer_class = UserReviewsSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = ReviewPagination

    def get_queryset(self):
        user = self.request.user
        reviews = Review.objects.filter(owner=user) 
        return reviews

    def list(self, request, *args, **kwargs):
        reviews = self.get_queryset()

        paginated_reviews = self.paginate_queryset(reviews)
        serializer = self.get_serializer(paginated_reviews, many=True)

        if reviews.exists(): 
            if paginated_reviews is not None:
                response = {
                    "count": self.paginator.page.paginator.count,
                    "next": self.paginator.get_next_link(),
                    "previous": self.paginator.get_previous_link(),
                    "data": serializer.data
                }
                return Response(data=response, status=status.HTTP_200_OK)
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        return Response({"detail": f"You dont howe any reviews {self.request.user.username}"}, status=status.HTTP_200_OK)
    

class ReviewCreateAPIView(generics.CreateAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        book_id = self.kwargs.get("pk")
        user = self.request.user

        book_obj = get_object_or_404(Book, id=book_id)

        if Review.objects.filter(book=book_obj, owner=user).exists():
            raise ValidationError("You have already review this book")
        
        serializer.save(book=book_obj, owner=user)

        return super().perform_create(serializer)


class ReviewListForBookAPIView(generics.ListAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticated]
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
    permission_classes = [IsAuthenticated, OwnerOrReadOnly]

 

"""ACCOUNTS VIEWS"""

class UserProfileAPIView(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = "username"

    def get(self, request, *args, **kwargs):
        instance = request.user
        username = kwargs.get("username")
        serializer = self.get_serializer(instance)

        if instance.username != username:
            return Response({"detail": "NOT ALLOWED"}, status=status.HTTP_403_FORBIDDEN)
        
        return Response(serializer.data)



class MyObtainTokenPAir(TokenObtainPairView):
    permission_classes = [AllowAny]
    serializer_class = MyTokenObtainPairSerializer


class RegisterUserAPIView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterUserSerializer
    permission_classes = [AllowAny]


class ChangePasswordAPIView(generics.UpdateAPIView):
    queryset = User.objects.all()
    serializer_class = ChangePasswordSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = "username"

    def get_object(self):
        username = self.request.user.username
        return get_object_or_404(User, username=username)
    

    def update(self, request, *args, **kwargs):
        username = kwargs.get("username")
        instance = self.get_object()
        if instance.username != username:
            return Response({"detail": "NOT ALLOWED"}, status=status.HTTP_403_FORBIDDEN)
        
        serializer = self.get_serializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response({"detail" : "Password changed successfully "}, status=status.HTTP_200_OK)
    

class UpdateProfileAPIView(generics.RetrieveUpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UpdateUserProfileSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = "username"


    def get(self, request, *args, **kwargs):
        instance = request.user
        username = self.kwargs["username"]
        serializer = self.get_serializer(instance)
        if instance.username != username:
            return Response({"detail": "NOT ALLOWED"}, status=status.HTTP_403_FORBIDDEN )
        return Response(serializer.data)

    
    def update(self, request, *args, **kwargs): 
        username = kwargs.get("username")
        instance = request.user

        if instance.username != username:
            return Response({"detail": "NOT ALLOWED"}, status=status.HTTP_403_FORBIDDEN)
        
        serializer = self.get_serializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        return Response({"detail": "Data updated successfully.", "data": serializer.data}, status=status.HTTP_200_OK)
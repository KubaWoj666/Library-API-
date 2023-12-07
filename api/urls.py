from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView
)


from . import views

urlpatterns = [
    path("authors/", views.AuthorListCreateAPIView.as_view(), name="authors-list"),
    path("authors/<int:pk>/", views.AuthorDetailAPIView.as_view(), name="author-detail"),

    path("books/", views.BookListCreateAPIView.as_view(), name="books-list"),
    path("books/<int:pk>/", views.BookDetailAPIView.as_view(), name="book-detail"),

    path("book/<int:pk>/review/", views.ReviewCreateAPIView.as_view(), name="review-create"),
    path('book/<int:pk>/all-reviews/', views.ReviewListForBookAPIView.as_view(), name='review-for-book'),
    path("review/<int:pk>/", views.ReviewDetailAPIView.as_view(), name="review-detail"),

    path('login/', views.MyObtainTokenPAir.as_view() , name='jwt-create'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('token/verify/', TokenVerifyView.as_view(), name='token_verify'),

    path("register/", views.RegisterUserAPIView.as_view(), name="register"),
    path("change-password/<str:username>/", views.ChangePasswordAPIView.as_view(), name="change-password")


]



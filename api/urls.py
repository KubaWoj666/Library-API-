from django.urls import path
from . import views

urlpatterns = [
    path("authors/", views.AuthorListCreateAPIView.as_view(), name="authors-list"),
    path("authors/<int:pk>/", views.AuthorDetailAPIView.as_view(), name="authors-detail"),

]
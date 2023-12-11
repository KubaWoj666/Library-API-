from typing import Any
from django.db import models
from django.core.validators import MinLengthValidator, MinValueValidator, MaxValueValidator
from accounts.models import User


class Author(models.Model):
    name = models.CharField(max_length=120)
    last_name = models.CharField(max_length=120)
    bio = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to="author_img", default="dp.png")
    birth_date = models.DateField(blank=True, null=True)
    death_date = models.DateField(blank=True, null=True)

    def __str__(self):
        return f"{self.name} {self.last_name}"
    


class BookManager(models.Manager):
    def create(self, **kwargs): 
        isbn = kwargs.get("ISBN")
        isbn = f"{isbn[0:3]}-{isbn[3:5]}-{isbn[5:11]}-{isbn[11]}-{isbn[12]}"
        kwargs.pop("ISBN")
        return super().create(ISBN=isbn, **kwargs)
        

class Book(models.Model):
    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name="written_books")
    title = models.CharField(max_length=120)
    image = models.ImageField(upload_to="book_image", default="blank.jpeg", blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    published = models.DateField(blank=True, null=True)
    ISBN = models.CharField(validators=[MinLengthValidator(13)], max_length=13, unique=True)

    objects = BookManager()

    def __str__(self):
        return self.title
    

class Review(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name="reviews")
    body = models.TextField(blank=True, null=True)
    rating = models.PositiveIntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)], blank=True, null=True) 
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.owner} {self.book}"
    
    

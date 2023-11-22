from django.db import models


class Author(models.Model):
    name = models.CharField(max_length=120)
    last_name = models.CharField(max_length=120)
    bio = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to="author_img", default="dp.png")
    birth_date = models.DateField(blank=True, null=True)
    death_date = models.DateField(blank=True, null=True)

    def __str__(self):
        return f"{self.name} {self.last_name}"


class Book(models.Model):
    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name="written_books")
    title = models.CharField(max_length=120)
    description = models.TextField(blank=True, null=True)
    published = models.DateField(blank=True, null=True)
    ISBN = models.CharField(max_length=13, unique=True)

    def __str__(self):
        return self.title

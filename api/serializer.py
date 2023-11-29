from django.urls import reverse
from django.db.models import Avg
from rest_framework import serializers

from books.models import Author, Book, Review






""" REVIEW SERIALIZERS"""

class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ["owner", "body", "rating"]



""" AUTHOR SERIALIZERS """
class AuthorSerializer(serializers.ModelSerializer):
    details = serializers.HyperlinkedIdentityField(view_name="author-detail", lookup_field="pk", )
    class Meta:
        model = Author
        fields = ["name", "last_name", "details"]


class AuthorCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = "__all__"


class AuthorDetailSerializer(serializers.ModelSerializer):
    written_books = serializers.StringRelatedField(many=True, read_only=True)
    class Meta:
        model = Author
        fields = ["id", "name", "last_name", "bio", "birth_date", "death_date", "image", "written_books" ]
    


""" BOOKS SERIALIZERS"""
class BookSerializer(serializers.ModelSerializer):
    book_author = serializers.SerializerMethodField(read_only=True)
    detail = serializers.HyperlinkedIdentityField(view_name="book-detail", lookup_field="pk")
    add_review = serializers.HyperlinkedIdentityField(view_name="review-create", lookup_field="pk")
    average_rating = serializers.SerializerMethodField()
    review_quantity = serializers.SerializerMethodField()

    class Meta:
        model = Book
        fields = ["id", "title", "book_author", "detail", "add_review", "average_rating", "review_quantity"]

    def get_book_author(self, obj):
        return f"{obj.author.name} {obj.author.last_name}"
    
    def get_average_rating(self, obj):
        review = Review.objects.filter(book=obj)
        avg = review.aggregate(Avg("rating", default=0)) 
        return avg["rating__avg"]
    
    def get_review_quantity(self, obj):
        review_count = Review.objects.filter(book=obj).count()
        return review_count
    

class BookCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = "__all__"


class BookDetailSerializer(serializers.ModelSerializer):
    author = AuthorSerializer()
    reviews = ReviewSerializer(many=True, read_only=True)
    class Meta:
        model = Book
        fields = "__all__"

    def get_book_author(self, obj):
        return f"{obj.author.name} {obj.author.last_name}"
    
    def update(self, instance, validated_data):

        # Author data update
        author_data = validated_data.get('author', None)
        if author_data:
            author_instance = instance.author
            author_serializer = AuthorSerializer(author_instance, data=author_data)
            if author_serializer.is_valid():
                author_serializer.save()

        # Rest of book data update
        instance.title = validated_data.get('title', instance.title)
        instance.description = validated_data.get('description', instance.description)
        instance.published = validated_data.get('published', instance.published)
        instance.ISBN = validated_data.get('ISBN', instance.ISBN)
        instance.save()

        return instance




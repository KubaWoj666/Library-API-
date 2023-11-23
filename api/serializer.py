from rest_framework import serializers

from books.models import Author, Book



class AuthorSerializer(serializers.ModelSerializer):
    details = serializers.HyperlinkedIdentityField(view_name="author-detail", lookup_field="pk")
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
    class Meta:
        model = Book
        fields = ["title", "book_author", "detail"]

    def get_book_author(self, obj):
        return f"{obj.author.name} {obj.author.last_name}"
    

class BookCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = "__all__"


class BookDetailSerializer(serializers.ModelSerializer):
    author = AuthorSerializer()
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




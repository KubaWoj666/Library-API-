from rest_framework import serializers

from books.models import Author, Book





class BookSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField(read_only=True)
    class Meta:
        model = Book
        fields = "__all__"


class AuthorSerializer(serializers.ModelSerializer):
    details = serializers.HyperlinkedIdentityField(view_name="authors-detail", lookup_field="pk")
    class Meta:
        model = Author
        fields = ["name", "last_name", "details"]


class AuthorDetailSerializer(serializers.ModelSerializer):
    written_books = serializers.StringRelatedField(many=True, read_only=True)
    class Meta:
        model = Author
        fields = "__all__"
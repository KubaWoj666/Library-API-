from django.urls import reverse
from django.db.models import Avg
from django.contrib.auth.password_validation import validate_password

from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.tokens import Token

from books.models import Author, Book, Review
from accounts.models import User







""" REVIEW SERIALIZERS"""

class ReviewSerializer(serializers.ModelSerializer):
    owner = serializers.CharField(read_only=True)
    class Meta:
        model = Review
        fields = ["owner" ,"body", "rating"]

    



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



"""ACCOUNTS SERIALIZERS"""


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user) -> Token:
        token =  super(MyTokenObtainPairSerializer, cls).get_token(user)

        token["username"] = user.username
        token["email"] = user.email

        return token


class RegisterUserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True, validators=[UniqueValidator(queryset=User.objects.all())])
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ['username', 'password', 'password2', 'email',]

    def validate(self, attrs):
        if attrs["password"] != attrs["password2"]:
            raise serializers.ValidationError({"password": "Password fields didn't match!"})
        return attrs

    def create(self, validated_data):
        user = User.objects.create(
            username = validated_data.get("username"),
            email = validated_data.get("email")
        )

        user.set_password(validated_data.get("password"))
        user.save()

        return user
    


# class ChangePasswordSerializer(serializers.ModelSerializer):
#     password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
#     password2 = serializers.CharField(write_only=True, required=True)
#     old_password = serializers.CharField(write_only=True, required=True)

#     class Meta:
#         model = User
#         fields = ["old_password", "password", "password2"]
        
#     # def create(self, validated_data):
#     #     old_password = validated_data.pop("old_password")
#     #     obj =  super().create(validated_data)
#     #     print(old_password)
#     #     return obj

#     def validate(self, attrs):
#         if attrs["password"] != attrs["password2"]:
#             raise serializers.ValidationError({"password":"Password fields didn't match!"})
        
#         return attrs
    
#     def validate_old_password(self, value):
#         user = self.context["request"].user

#         if not user.check_password(value):
#             raise serializers.ValidationError({"old password": "Old password is not correct!"})
        
#         return value
    
#     def update(self, instance, validated_data): 
#         instance.set_password(validated_data.get("password"))
#         instance.save()

#         return instance

from django.contrib.auth.hashers import check_password

# class ChangePasswordSerializer(serializers.Serializer):
#     old_password = serializers.CharField(write_only=True, required=True)
#     password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
#     password2 = serializers.CharField(write_only=True, required=True)

#     def validate_old_password(self, value):
#         user = self.context["request"].user

#         if not check_password(value, user.password):
#             raise serializers.ValidationError({"old_password": "Old password is not correct!"})

#         return value

#     def validate(self, attrs):
#         if attrs["password"] != attrs["password2"]:
#             raise serializers.ValidationError({"password": "Password fields didn't match!"})

#         return attrs

#     def update(self, instance, validated_data): 
#         instance.set_password(validated_data.get("password"))
#         instance.save()

#         return instance

class ChangePasswordSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)
    old_password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ('old_password', 'password', 'password2')
        lookup_field = "username"


    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})

        return attrs

    def validate_old_password(self, value):
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError({"old_password": "Old password is not correct"})
        return value

    def update(self, instance, validated_data):

        instance.set_password(validated_data['password'])
        instance.save()

        return instance
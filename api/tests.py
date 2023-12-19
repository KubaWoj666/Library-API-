from rest_framework.test import APITestCase, APIRequestFactory
from rest_framework import status

from django.urls import reverse
from django.contrib.auth import get_user_model

from datetime import date

from books.models import Book, Author, Review



User = get_user_model()


class AuthorApiViews(APITestCase):
    def setUp(self) -> None:
        self.url = reverse("authors-list")

        self.superuser = User.objects.create_superuser(username="Superuser", email="super@email.com", password="testpassword")

        # self.user = User.objects.create(username="Test", email="test@email.com", password="password")

        self.author = Author.objects.create(name="Test", last_name="Author", bio="test bio", birth_date=date(1999, 12, 12))

        self.book = Book.objects.create(title="Test Title", description="Test description", published=date(2023, 12, 12), ISBN="1234567890123", author=self.author)


    def authenticate_admin(self):
        response = self.client.post(reverse("jwt-create"), {"email": "super@email.com", "password": "testpassword"})
        # print(response.data)
        token = response.data["access"]
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")
    

    def authenticate(self):
        self.client.post(reverse("register"), {"username": "test", "email": "test@email.com", "password":"testpassword", "password2":"testpassword"})

        response = self.client.post(reverse("jwt-create"),{"email": "test@email.com", "password":"testpassword"})
        # print(response.data['access'])
        token = response.data["access"]

        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")


    def test_author_list_get(self):
        self.authenticate()
        response = self.client.get(self.url)
        # print(response.data["results"])
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], 1)
        self.assertEqual(response.data["results"][0]["name"], "Test")
        self.assertEqual(response.data["results"][0]["last_name"], "Author")
    

    def test_author_list_get_unauthenticated(self):
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)   


    def test_author_list_create_by_admin(self):
        data = {
            "name": "NewTest", 
            "last_name": "Author", 
            "bio": "test bio", 
            "birth_date": date(1999, 10, 12),
        }
        self.authenticate_admin()
        response = self.client.post(self.url, data)
        # print(response.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["id"], 2)
        self.assertEqual(response.data["name"], "NewTest")
        self.assertEqual(response.data["last_name"], "Author")
        self.assertEqual(response.data["bio"], "test bio")
        self.assertEqual(response.data["birth_date"], "1999-10-12")


    def test_author_list_create_by_user(self):
        data = {
            "name": "NewTest", 
            "last_name": "Author", 
            "bio": "test bio", 
            "birth_date": date(1999, 10, 12),
        }

        self.authenticate()

        response = self.client.post(self.url, data)
        # print(response.data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


    def test_author_detail_get(self):
        self.authenticate()

        response = self.client.get(reverse("author-detail", kwargs={"pk": 1}))
        # print(response.data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["id"], 1)
        self.assertEqual(response.data["name"], "Test")
        self.assertEqual(response.data["last_name"], "Author")
        self.assertEqual(response.data["bio"], "test bio")
        self.assertEqual(response.data["birth_date"], "1999-12-12")
        self.assertEqual(response.data["written_books"], ['Test Title'])


    def test_author_by_admin_update(self):
        data={
            "name": "Update", 
            "last_name": "Update last name", 
            "bio": "update bio", 
            "birth_date": date(1999, 10, 2),
        }

        self.authenticate_admin()

        response = self.client.put(reverse("author-detail", kwargs={"pk":1}), data=data)
        # print(response.data)

        self.assertEqual(response.data["name"], "Update")
        self.assertEqual(response.data["last_name"], "Update last name")
        self.assertEqual(response.data["bio"], "update bio")
        self.assertEqual(response.data["birth_date"], "1999-10-02")
        self.assertEqual(response.data["written_books"], ['Test Title'])


    def test_author_update_by_user(self):
        data={
            "name": "Update", 
            "last_name": "Update last name", 
            "bio": "update bio", 
            "birth_date": date(1999, 10, 2),
        }
        self.authenticate()

        response = response = self.client.put(reverse("author-detail", kwargs={"pk":1}), data=data)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


    def test_author_delete_by_admin(self):
        self.authenticate_admin()

        response = self.client.delete(reverse("author-detail", kwargs={"pk":1}))

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


    def test_author_delete_by_user(self):
        self.authenticate()

        response = self.client.delete(reverse("author-detail", kwargs={"pk":1}))

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)



class BooksApiViews(APITestCase):
    def setUp(self) -> None:
        self.book_list_url = reverse("books-list")
        self.book_detail_url = reverse("book-detail", kwargs={"pk":1})

        self.superuser = User.objects.create_superuser(username="Superuser", email="super@email.com", password="testpassword")

        # self.user = User.objects.create(username="Test", email="test@email.com", password="password")

        self.author = Author.objects.create(name="Test", last_name="Author", bio="test bio", birth_date=date(1999, 12, 12))

        self.book = Book.objects.create(title="Test Title", description="Test description", published=date(2023, 12, 12), ISBN="1234567890123", author=self.author)


    def authenticate_admin(self):
        response = self.client.post(reverse("jwt-create"), {"email": "super@email.com", "password": "testpassword"})
        # print(response.data)
        token = response.data["access"]
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")
    

    def authenticate(self):
        self.client.post(reverse("register"), {"username": "test", "email": "test@email.com", "password":"testpassword", "password2":"testpassword"})

        response = self.client.post(reverse("jwt-create"),{"email": "test@email.com", "password":"testpassword"})
        # print(response.data['access'])
        token = response.data["access"]

        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")


    def test_book_list_get(self):
        self.authenticate()

        response = self.client.get(self.book_list_url)
        # print(response.data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], 1)
        self.assertEqual(response.data["results"][0]["title"], "Test Title")
        self.assertEqual(response.data["results"][0]["book_author"], "Test Author")
    
    def test_book_list_get_unauthorize(self):

        response = self.client.get(self.book_list_url)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    
    def test_book_list_create_by_admin(self):
        data = {
            "title": "Test Title",
            "description": "Test description",
            "published": date(2023, 12, 12),
            "ISBN": "1234567890124",
            "author": self.author.id
        }

        self.authenticate_admin()
        response = self.client.post(self.book_list_url, data=data)

        # print(response.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["id"], 2)
        self.assertEqual(response.data["title"], "Test Title")
        self.assertEqual(response.data["description"], "Test description")
        self.assertEqual(response.data["published"], "2023-12-12")
        self.assertEqual(response.data["ISBN"], "123-45-678901-2-4")
        self.assertEqual(response.data["author"], 1)


    def test_book_list_create_by_user(self):
        data = {
            "title": "Test Title",
            "description": "Test description",
            "published": date(2023, 12, 12),
            "ISBN": "1234567890124",
            "author": self.author.id
        }

        self.authenticate()
        response = self.client.post(self.book_list_url, data=data)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
    

    def test_book_detail(self):
        self.authenticate()
        response = self.client.get(self.book_detail_url)
        # print(response.data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["id"], 1)
        self.assertEqual(response.data["author"]["name"], "Test")
        self.assertEqual(response.data["reviews"], [])
        self.assertEqual(response.data["title"], "Test Title")
        self.assertEqual(response.data["description"], "Test description")
        self.assertEqual(response.data["published"], "2023-12-12")
        self.assertEqual(response.data["ISBN"], "123-45-678901-2-3")
    
    def test_book_detail(self):
        response = self.client.get(self.book_detail_url)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_update_book_by_admin(self):
        data = {
            "id": 12,
            "author": {
                "name": "Update Name",
                "last_name": "Update Last Name"
            },
            "title": "Updated Title",
            "description": "Updated description",
            "published": "2022-12-11",
            "ISBN": "3333333333334"
        }
        

        self.authenticate_admin()

        response = self.client.put(self.book_detail_url, data=data, format="json")
        # print (response.data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["id"], 1)
        self.assertEqual(response.data["author"]["name"], "Update Name")
        self.assertEqual(response.data["reviews"], [])
        self.assertEqual(response.data["title"], "Updated Title")
        self.assertEqual(response.data["description"], "Updated description")
        self.assertEqual(response.data["published"], "2022-12-11")
        self.assertEqual(response.data["ISBN"], "3333333333334")
    

    def test_update_book_by_user(self):
        data = {
            "id": 12,
            "author": {
                "name": "Update Name",
                "last_name": "Update Last Name"
            },
            "title": "Updated Title",
            "description": "Updated description",
            "published": "2022-12-11",
            "ISBN": "3333333333334"
        }
        self.authenticate()

        response = self.client.put(self.book_detail_url, data=data, format="json")

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


    def test_delete_book_by_admin(self):
        self.authenticate_admin()

        response = self.client.delete(self.book_detail_url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
    
    def test_delete_book_by_user(self):
        self.authenticate()

        response = self.client.delete(self.book_detail_url)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
    

    def test_delete_book_by_unauthenticated_user(self):
        response = self.client.delete(self.book_detail_url)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class ReviewsAPIViews(APITestCase):
    def setUp(self) -> None:
        self.review_create_url = reverse("review-create", kwargs={"pk":1})
        self.all_reviews_for_book_url = reverse("review-for-book", kwargs={"pk":1})
        self.review_detail = reverse("review-detail", kwargs={"pk":1})
        self.user_reviews = reverse("user_review")

        self.superuser = User.objects.create_superuser(username="Superuser", email="super@email.com", password="testpassword")

        self.user = User.objects.create_user(username="Test", email="test@email.com", password="password")

        self.author = Author.objects.create(name="Test", last_name="Author", bio="test bio", birth_date=date(1999, 12, 12))

        self.book = Book.objects.create(title="Test Title", description="Test description", published=date(2023, 12, 12), ISBN="1234567890123", author=self.author)

        # self.review = Review.objects.create(owner=self.user, book=self.book, body="Test review", rating=5)

    def authenticate(self):
        response = self.client.post(reverse("jwt-create"), {"email":"test@email.com", "password": "password"})
       
        token = response.data["access"]
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")


    def test_review_create(self):
        data = {
            "body": "test body",
            "rating": 5,
            }

        self.authenticate()
        
        response = self.client.post(self.review_create_url, data=data)
        # print(response.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["owner"], "Test")
        self.assertEqual(response.data["body"], "test body")
        self.assertEqual(response.data["rating"], 5)

    def test_review_create_unauthenticated_user(self):
        data = {
            "body": "test body",
            "rating": 5,
            }

        response = self.client.post(self.review_create_url, data=data)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
    

    def test_review_create_invalid_data(self):
        data = {
            "body": "test body",
            "rating": -1,
            }

        self.authenticate()

        response = self.client.post(self.review_create_url, data=data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    
    def test_review_create_same_user__for_same_book(self):
        Review.objects.create(owner=self.user, book=self.book, body="Test review", rating=5)

        data = {
            "body": "test body",
            "rating": 5,
            }

        self.authenticate()
        
        response = self.client.post(self.review_create_url, data=data)
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data[0], "You have already review this book")


    def test_all_review_for_book(self):
        self.authenticate()
        Review.objects.create(owner=self.user, book=self.book, body="Test review", rating=5)

        response = self.client.get(self.all_reviews_for_book_url)
        # print(response.data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["message"], "Reviews for 'Test Title'. ")
        self.assertEqual(response.data["data"][0]["owner"], "Test")
        self.assertEqual(response.data["data"][0]["body"], "Test review")
        self.assertEqual(response.data["data"][0]["rating"], 5)


    def test_review_detail(self):
        Review.objects.create(owner=self.user, book=self.book, body="Test review", rating=5)
        self.authenticate()

        response = self.client.get(self.review_detail)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["owner"], "Test")
        self.assertEqual(response.data["body"], "Test review")
        self.assertEqual(response.data["rating"], 5)
    
    def test_review_update(self):
        Review.objects.create(owner=self.user, book=self.book, body="Test review", rating=5)
        self.authenticate()

        data = {
            "body": "Updated body",
            "rating": "1"
        }

        response = self.client.put(self.review_detail, data=data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["owner"], "Test")
        self.assertEqual(response.data["body"], "Updated body")
        self.assertEqual(response.data["rating"], 1)
    

    def test_review_updated_by_not_a_review_owner(self):
        User.objects.create_user(username="New", email="new@email.com", password="password")
        Review.objects.create(owner=self.user, book=self.book, body="Test review", rating=5)

        login = self.client.post(reverse("jwt-create"), {"email": "new@email.com", "password":"password"})

        token = login.data["access"]
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")

        data = {
            "body": "Updated body",
            "rating": "1"
        }

        response = self.client.put(self.review_detail, data=data)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response.data["detail"], "You do not have permission to perform this action.")

    def test_user_reviews(self):
        Review.objects.create(owner=self.user, book=self.book, body="Test review 1", rating=5)
        Review.objects.create(owner=self.user, book=self.book, body="Test review 2", rating=1)

        self.authenticate()

        response = self.client.get(self.user_reviews)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], 2)
        self.assertEqual(response.data["data"][0]["book"], "Test Title")
        self.assertEqual(response.data["data"][0]["body"], "Test review 1")
        self.assertEqual(response.data["data"][0]["rating"], 5)
        self.assertEqual(response.data["data"][1]["book"], "Test Title")
        self.assertEqual(response.data["data"][1]["body"], "Test review 2")
        self.assertEqual(response.data["data"][1]["rating"], 1)









        











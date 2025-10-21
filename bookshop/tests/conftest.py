import pytest
from rest_framework.test import APIClient
from django.contrib.auth.models import User
from bookshop.models import Book, Publisher, Author
from django.utils import timezone

@pytest.fixture(scope="function")
def api_client():
    yield APIClient()

@pytest.fixture
def user(db):
    return User.objects.create_user(username="user228", password="password")


@pytest.fixture
def auth_client(api_client, user):
    api_client.force_authenticate(user=user)
    return api_client


@pytest.fixture
def publisher(db):
    return Publisher.objects.create(name="publisher")


@pytest.fixture
def author(db):
    return Author.objects.create(name = "random name")


@pytest.fixture
def book(db, publisher, author):
    b = Book.objects.create(
        title="random book",
        description="description",
        price=100,
        publisher=publisher,
        pages=100,
        rating=5,
        created_at =timezone.now(),
    )
    b.authors.add(author)
    return b

import pytest
from rest_framework import status

@pytest.mark.django_db
def test_booklist_get(api_client):
    response = api_client.get("/books/")
    assert response.status_code == 200

@pytest.mark.django_db
def test_get_books_list(api_client, book):
    response = api_client.get("/books/")
    assert response.status_code == status.HTTP_200_OK
    assert len(response.data["data"]) == 1
    assert response.data["data"][0]["title"] == "random book"


@pytest.mark.django_db
def test_get_single_book(api_client, book):
    response = api_client.get(f"/books/{book.id}/")
    assert response.status_code == status.HTTP_200_OK
    assert response.data["title"] == book.title


@pytest.mark.django_db
def test_get_book_filter_by_publisher(api_client, publisher, book):
    response = api_client.get(f"/books/?publisherId={publisher.id}")
    assert response.status_code == status.HTTP_200_OK
    assert response.data["data"][0]["publisher"]["id"] == publisher.id


@pytest.mark.django_db
def test_create_book_requires_authentication(api_client, publisher):
    data = {
        "title": "Book",
        "price": 50,
        "publisher_id": publisher.id,
    }
    response = api_client.post("/books/", data, format="json")
    assert response.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.django_db
def test_create_book_invalid_fields(auth_client):
    data = {
        "title": "",  # invalid 
        "price": "string",  # invalid 
    }
    response = auth_client.post("/books/", data, format="json")
    assert response.status_code == status.HTTP_400_BAD_REQUEST

@pytest.mark.django_db
def test_update_book(auth_client, book):
    data = {"title": "Updated Title"}
    response = auth_client.put(f"/books/{book.id}/", data, format="json")
    assert response.status_code == status.HTTP_200_OK
    book.refresh_from_db()
    assert book.title == "Updated Title"


@pytest.mark.django_db
def test_update_book_unauthorized(api_client, book):
    data = {"title": "Hacker Edit"}
    response = api_client.put(f"/books/{book.id}/", data, format="json")
    assert response.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.django_db
def test_update_nonexistent_book(auth_client):
    data = {"title": "Does Not Exist"}
    response = auth_client.put("/books/99999/", data, format="json")
    assert response.status_code == status.HTTP_404_NOT_FOUND


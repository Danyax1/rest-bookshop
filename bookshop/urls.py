from django.urls import path
from django.http import JsonResponse
from .views import (
    BookListCreateAPIView, BookDetailAPIView,
    AuthorListCreateAPIView, AuthorDetailAPIView,
    PublisherListCreateAPIView, PublisherDetailAPIView
)

def api_root(request):
    return JsonResponse({"message": "Welcome to the Bookshop API"})

urlpatterns = [
    path('', api_root, name='api-root'),
    path('books/', BookListCreateAPIView.as_view(), name='books-list'),
    path('books/<int:pk>/', BookDetailAPIView.as_view(), name='books-detail'),
    path('authors/', AuthorListCreateAPIView.as_view(), name='authors-list'),
    path('authors/<int:pk>/', AuthorDetailAPIView.as_view(), name='authors-detail'),
    path('publishers/', PublisherListCreateAPIView.as_view(), name='publishers-list'),
    path('publishers/<int:pk>/', PublisherDetailAPIView.as_view(), name='publishers-detail'),
]

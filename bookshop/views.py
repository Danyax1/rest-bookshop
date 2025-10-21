from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from .models import Book, Author, Publisher, User
from .serializers import BookListSerializer, BookDetailSerializer, AuthorSerializer, PublisherSerializer, UserSerializer

class BookListCreateAPIView(APIView):
    def get_permissions(self):
        if self.request.method == 'POST':
            return [IsAuthenticated()]
        return [AllowAny()]
    def get(self, request):
        publisher_id = request.query_params.get('publisherId')
        genre = request.query_params.get('genre')

        query_param = Book.objects.all().prefetch_related('authors','genres','publisher')

        if publisher_id:
            query_param = query_param.filter(publisher_id=publisher_id)

        serializer = BookListSerializer(query_param, many=True)
        return Response({'data': serializer.data})

    def post(self, request):
        data = request.data
        serializer = BookDetailSerializer(data=data)
        if serializer.is_valid():
            book = Book.objects.create(
                title=data['title'],
                description=data.get('description',''),
                isbn=data.get('isbn',''),
                publisher_id=data.get('publisher_id'),
                price=data['price'],
                currency=data.get('currency','UAH'),
                stock=data.get('stock',0),
                pages=data.get('pages'),
                published_date=data.get('published_date'),
                cover_url=data.get('cover_url',''),
                rating=data.get('rating')
            )

            author_ids = data.get('authors', [])
            if author_ids:
                book.authors.add(*author_ids)

            genre_ids = data.get('genres_ids', [])
            if genre_ids:
                book.genres.add(*genre_ids)
            resp = BookDetailSerializer(book)
            return Response(resp.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class BookDetailAPIView(APIView):
    def get_permissions(self):
        if self.request.method == 'PUT':
            return [IsAuthenticated()]
        return [AllowAny()]
    def get(self, request, pk):
        book = get_object_or_404(Book, pk=pk)
        return Response(BookDetailSerializer(book).data)

    def put(self, request, pk):
        book = get_object_or_404(Book, pk=pk)
        serializer = BookDetailSerializer(book, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()

            if 'authors' in request.data:
                book.authors.set(request.data['authors'])
            if 'genres' in request.data:
                book.genres.set(request.data['genres'])
            return Response(BookDetailSerializer(book).data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AuthorListCreateAPIView(APIView):
    def get_permissions(self):
        if self.request.method == 'POST':
            return [IsAuthenticated()]
        return [AllowAny()]
    def get(self, request):
        authors = Author.objects.all()

        serializer = AuthorSerializer(authors, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = AuthorSerializer(data=request.data)
        if serializer.is_valid():
            author = serializer.save()
            return Response(AuthorSerializer(author).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class AuthorDetailAPIView(APIView):
    def get_permissions(self):
        if self.request.method == 'PUT' or self.request.method == 'DELETE':
            return [IsAuthenticated()]
        return [AllowAny()]
    def get(self, request, pk):
        author = get_object_or_404(Author, pk=pk)
        data = AuthorSerializer(author).data

        books = author.books.all()
        data['books'] = BookListSerializer(books, many=True).data
        return Response(data)

    def post(self, request, pk):
        author = get_object_or_404(Author, pk=pk)
        serializer = AuthorSerializer(author, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(AuthorSerializer(author).data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, pk):
        author = get_object_or_404(Author, pk=pk)
        if author.books.exists():
            return Response(
                {"error":"Author has books"},
                status=status.HTTP_400_BAD_REQUEST)
        author.delete()
        return Response(status=status.HTTP_200_OK)


class PublisherListCreateAPIView(APIView):
    def get_permissions(self):
        if self.request.method == 'POST':
            return [IsAuthenticated()]
        return [AllowAny()]
    def get(self, request):
        publishers = Publisher.objects.all()
        serializer = PublisherSerializer(publishers, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = PublisherSerializer(data=request.data)
        if serializer.is_valid():
            pub = serializer.save()
            return Response(PublisherSerializer(pub).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class PublisherDetailAPIView(APIView):
    def get(self, request, pk):
        publisher = get_object_or_404(Publisher, pk=pk)
        data = PublisherSerializer(publisher).data
        data['books'] = BookListSerializer(publisher.books.all(), many=True).data
        return Response(data)

    def post(self, request, pk):
        publisher = get_object_or_404(Publisher, pk=pk)
        serializer = PublisherSerializer(publisher, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(PublisherSerializer(publisher).data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        publisher = get_object_or_404(Publisher, pk=pk)
        publisher.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
class UserDetailAPIView(APIView):
    def get(self, request, pk):
        user_data = get_object_or_404(User, pk=pk)
        serializers = UserDetailAPIView(user_data).data
        return Response({"User":serializers})


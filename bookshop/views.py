from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from .models import Book, Author, Publisher
from .serializers import BookListSerializer, BookDetailSerializer, AuthorSerializer, PublisherSerializer
from django.db.models import Q

# Books list / create
class BookListCreateAPIView(APIView):
    def get(self, request):
        q = request.query_params.get('q')
        publisher_id = request.query_params.get('publisherId')
        genre = request.query_params.get('genre')
        sort = request.query_params.get('sort') 

        qs = Book.objects.all().prefetch_related('authors','genres','publisher')

        if q:
            qs = qs.filter(Q(title__icontains=q) | Q(authors__name__icontains=q)).distinct()

        if publisher_id:
            qs = qs.filter(publisher_id=publisher_id)

        if genre:
            qs = qs.filter(genres__name__iexact=genre)

        if sort == 'price_asc':
            qs = qs.order_by('price')
        elif sort == 'price_desc':
            qs = qs.order_by('-price')
        elif sort == 'title_asc':
            qs = qs.order_by('title')
        elif sort == 'title_desc':
            qs = qs.order_by('-title')

        serializer = BookListSerializer(qs, many=True)
        return Response({'data': serializer.data})

    def post(self, request):
        # minimal create - expects authors as list of ids, publisher_id, genres as list of names/ids
        data = request.data
        serializer = BookDetailSerializer(data=data)
        # We'll create manually to support m2m via ids:
        if serializer.is_valid():
            # ideally use serializer.save with nested work; simplified:
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

    def delete(self, request, pk):
        book = get_object_or_404(Book, pk=pk)
        book.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class AuthorListCreateAPIView(APIView):
    def get(self, request):
        q = request.query_params.get('q')
        qs = Author.objects.all()
        if q:
            qs = qs.filter(name__icontains=q)

        serializer = AuthorSerializer(qs, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = AuthorSerializer(data=request.data)
        if serializer.is_valid():
            author = serializer.save()
            return Response(AuthorSerializer(author).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class AuthorDetailAPIView(APIView):
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

    def delete(self, request, pk):
        author = get_object_or_404(Author, pk=pk)
        if author.books.exists():
            return Response(
                {"error":"Cannot delete author while they have books on the site. Remove or reassign books first."},
                status=status.HTTP_400_BAD_REQUEST
            )
        author.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# Publishers
class PublisherListCreateAPIView(APIView):
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
        pub = get_object_or_404(Publisher, pk=pk)
        data = PublisherSerializer(pub).data
        data['books'] = BookListSerializer(pub.books.all(), many=True).data
        return Response(data)

    def post(self, request, pk):
        pub = get_object_or_404(Publisher, pk=pk)
        serializer = PublisherSerializer(pub, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(PublisherSerializer(pub).data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        pub = get_object_or_404(Publisher, pk=pk)
        # simple business rule: either prevent or set book.publisher to null
        if pub.books.exists():
            return Response(
                {"error":"Author has books"},
                status=status.HTTP_400_BAD_REQUEST
            )
        pub.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

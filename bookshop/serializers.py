from rest_framework import serializers
from .models import Book, Author, Publisher, Genre

class AuthorSerializer(serializers.ModelSerializer):
    book_count = serializers.IntegerField(source='books.count')

    class Meta:
        model = Author
        fields = ['id','name','bio','photo_url','book_count']

class PublisherSerializer(serializers.ModelSerializer):
    class Meta:
        model = Publisher
        fields = ['id','name','description','website']

class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ['id','name']

class BookListSerializer(serializers.ModelSerializer):
    authors = AuthorSerializer(many=True)
    publisher = PublisherSerializer()
    genres = GenreSerializer(many=True)

    class Meta:
        model = Book
        fields = ['id','title','authors','publisher','price','currency','stock','rating','genres','cover_url']

class BookDetailSerializer(serializers.ModelSerializer):
    authors = AuthorSerializer(many=True)
    publisher = PublisherSerializer()
    genres = GenreSerializer(many=True)

    class Meta:
        model = Book
        fields = '__all__'

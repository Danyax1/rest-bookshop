from django.db import models

class User(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(max_length=150)
    password_hash = models.CharField(max_length=500)
    role = models.CharField(max_length=20)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

class Author(models.Model):
    name = models.CharField(max_length=100)
    bio = models.TextField()
    photo_url = models.URLField(blank=True)

    def __str__(self):
        return self.name

class Genre(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

class Publisher(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    website = models.URLField(blank=True)

    def __str__(self):
        return self.name

class Book(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    isbn = models.CharField(max_length=20, blank=True)
    publisher = models.ForeignKey(Publisher, on_delete=models.SET_NULL, null=True, related_name='books')
    price = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=10)
    stock = models.IntegerField(default=0)
    pages = models.IntegerField()
    published_date = models.DateField(null=True, blank=True)
    cover_url = models.URLField(blank=True)
    rating = models.DecimalField(max_digits=3, decimal_places=2)
    created_at = models.DateTimeField()

    authors = models.ManyToManyField(Author, through='BookAuthor', related_name='books')
    genres = models.ManyToManyField(Genre, through='BookGenre', related_name='books')

    def __str__(self):
        return self.title

class BookAuthor(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)

class BookGenre(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE)

class Order(models.Model):
    STATUS_CHOICES = (
        ('created','created'),
        ('shipped','shipped'),
        ('cancelled','cancelled'),
    )
    user = models.ForeignKey(User,on_delete=models.CASCADE, related_name='orders')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='created')
    total_amount = models.DecimalField(max_digits=12, decimal_places=2)
    created_at = models.DateTimeField()

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    book = models.ForeignKey(Book, on_delete=models.PROTECT)
    quantity = models.PositiveIntegerField()
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)

class CartItem(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE, related_name='cart_items')
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)


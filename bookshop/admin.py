from django.contrib import admin

from .models import User, Author, Genre, Publisher, Book, BookAuthor, Order, OrderItem, CartItem, BookGenre

# Register your models here.

admin.site.register(User)
admin.site.register(Author)
admin.site.register(Genre)
admin.site.register(Publisher)
admin.site.register(Book)
admin.site.register(BookAuthor)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(CartItem)
admin.site.register(BookGenre)

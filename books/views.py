from rest_framework import generics, filters
from rest_framework.permissions import AllowAny, IsAuthenticated
from accounts.permissions import IsAdmin
from .models import Book
from .serializers import BookSerializer
# from rest_framework.parsers import (MultiPartParser, FormParser)


class BookListCreateView(generics.ListCreateAPIView):
    # parser_classes = (MultiPartParser, FormParser) # To handle image uploads
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [AllowAny]
    
    # Enable search
    filter_backends = [filters.SearchFilter]

    # Search fields
    search_fields = [
        'title',
        'author',
        'category',
        'isbn'
    ]

class BookDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
from rest_framework import generics, filters
from rest_framework.permissions import IsAuthenticated
from accounts.permissions import IsAdminOrLibrarian
from .models import Book
from .serializers import BookSerializer
# from rest_framework.parsers import (MultiPartParser, FormParser)


class BookListCreateView(generics.ListCreateAPIView):
    # parser_classes = (MultiPartParser, FormParser) # To handle image uploads
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    
    # Enable search
    filter_backends = [filters.SearchFilter]

    # Search fields
    search_fields = [
        'title',
        'author',
        'category',
        'isbn'
    ]

    def get_permissions(self):

        if self.request.method == 'GET':
            return [IsAuthenticated()]

        return [IsAdminOrLibrarian()]

class BookDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

    def get_permissions(self):

        if self.request.method == 'GET':
            return [IsAuthenticated()]

        return [IsAdminOrLibrarian()]
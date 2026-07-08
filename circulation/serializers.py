from rest_framework import serializers

from books.models import Book
from accounts.models import User
from .models import IssueBook

# Book information
class BookInfoSerializer(serializers.ModelSerializer):

    class Meta:
        model = Book
        fields = [
            "id",
            "title",
            "author",
        ]

# User information
class UserInfoSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "role",
        ]

# Used when creating a borrow request
class BorrowRequestSerializer(serializers.ModelSerializer):

    class Meta:
        model = IssueBook
        fields = [
            "id",
            "book",
        ]

# Used when reading issue records
class IssueBookSerializer(serializers.ModelSerializer):

    book = BookInfoSerializer(read_only=True)
    member = UserInfoSerializer(read_only=True)

    class Meta:
        model = IssueBook
        fields = "__all__"

# Serializer for direct issue by librarian/admin
class DirectIssueSerializer(serializers.ModelSerializer):

    class Meta:
        model = IssueBook

        fields = [
            "book",
            "member"
        ]
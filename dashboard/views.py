# DRF API View
from rest_framework.views import APIView
from rest_framework.response import Response

from rest_framework.permissions import IsAuthenticated
from accounts.permissions import IsAdminOrLibrarian, IsStudent

# Models
from django.db.models import Count
from books.models import Book
from accounts.models import User
from circulation.models import IssueBook
from datetime import date

class DashboardStatsView(APIView):

    permission_classes = [IsAdminOrLibrarian]

    def get(self, request):

        # Total books in library
        total_books = Book.objects.count()

        # Total registered members(students, librarian, admin)
        total_students = User.objects.filter(
        role="student"
        ).count()

        total_librarians = User.objects.filter(
            role="librarian"
        ).count()

        total_admins = User.objects.filter(
            role="admin"
        ).count()
        # Books currently issued
        books_issued = IssueBook.objects.filter(
            status='issued'
        ).count()

        # Overdue books
        overdue_books = IssueBook.objects.filter(
            status='issued',
            due_date__lt=date.today()
        ).count()

        return Response({
            "total_students": total_students,
            "total_librarians": total_librarians,
            "total_admins": total_admins,
            "books_issued": books_issued,
            "overdue_books": overdue_books,
        })

class RecentIssuesView(APIView):

    permission_classes = [IsAdminOrLibrarian]

    def get(self, request):

        issues = IssueBook.objects.order_by(
            '-issue_date'
        )[:5]

        data = []

        for issue in issues:

            data.append({

                "book": issue.book.title,
                "book_cover": issue.book.cover_image

                if issue.book.cover_image else None,

                "member": issue.member.full_name,
                "member_photo": issue.member.profile_picture.url

                if issue.member.profile_picture else None,

                "issue_date": issue.issue_date,
                "due_date": issue.due_date

            })

        return Response(data)
    
class PopularBooksView(APIView):

    permission_classes = [IsAdminOrLibrarian]

    def get(self, request):

        books = Book.objects.annotate(
            issue_count=
            Count('issuebook')
        ).order_by(
            '-issue_count'
        )[:5]

        data = []

        for book in books:

            data.append({

                "title": book.title,

                "author": book.author,

                "times_issued":book.issue_count,

                "cover_image":
                    book.cover_image
                    if book.cover_image
                    else None

            })

        return Response(data)
    
class NotificationsView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):
         
        notifications = []

        # 1. Issued Books

        recent_issues = IssueBook.objects.filter(
            status='issued'
        ).order_by('-id')

        for issue in recent_issues:

            notifications.append({
                "type": "issued",
                "message":
                f"{issue.member.full_name} issued '{issue.book.title}'",
                "date": issue.issue_date,
            })

        # 2. Returned Books
        returned_books = IssueBook.objects.filter(
                status='returned'
        ).order_by('-id')

        for issue in returned_books:

            notifications.append({
                "type": "returned",
                "message":
                f"{issue.member.full_name} returned '{issue.book.title}'",
                "date": issue.return_date,
            })      
        
        # 3. Overdue Books
        overdue_books = IssueBook.objects.filter(
            status='issued',
            due_date__lt=date.today()
        )

        for issue in overdue_books:

            notifications.append({

                "type": "overdue",

                "message":
                f"'{issue.book.title}' is overdue for {issue.member.full_name}",

                "date": issue.due_date

            })

        # 4. Low Stock Books
        low_stock_books = Book.objects.filter(
            available_copies__lte=1
        )

        for book in low_stock_books:

            notifications.append({

                "type": "low_stock",

                "message":
                f"Only {book.available_copies} copy left of '{book.title}'"

            })
            
        # Sort latest activity first
        notifications.sort(
            key=lambda x: x.get('date', date.min),
            reverse=True
        )

        return Response(notifications)  

class CategoryDistributionView(APIView):

    permission_classes = [IsAdminOrLibrarian]

    def get(self, request):

        categories = Book.objects.values(
            'category'
        ).annotate(
            total=Count('id')
        )

        return Response(categories)
    
class IssueReturnChartView(APIView):

    permission_classes = [IsAdminOrLibrarian]

    def get(self, request):

        issued = IssueBook.objects.filter(
            status='issued'
        ).count()

        returned = IssueBook.objects.filter(
            status='returned'
        ).count()

        return Response({
            "issued": issued,
            "returned": returned
        })
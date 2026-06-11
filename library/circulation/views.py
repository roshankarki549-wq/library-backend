from datetime import date, timedelta
from urllib import request

# Allow Admin and Librarian users
from library.library.accounts.permissions import IsAdminOrLibrarian

from rest_framework.views import APIView
from rest_framework import generics
from rest_framework import status
from rest_framework.response import Response

from library.library.books.models import Book
from members.models import Member

from .models import IssueBook
from .serializers import IssueBookSerializer
from rest_framework.views import APIView
from rest_framework.response import Response

from .reminders import send_overdue_reminders


class IssueBookCreateView(generics.CreateAPIView):
    
    # Only Admin or Librarian can issue books
    permission_classes = []

    # Serializer used for validation and saving
    serializer_class = IssueBookSerializer

    def create(self, request, *args, **kwargs):

        # Get book ID from request data
        book_id = request.data.get('book')

        # Get member ID from request data
        member_id = request.data.get('member')

        try:
            # Fetch book from database
            book = Book.objects.get(id=book_id)

        except Book.DoesNotExist:

            return Response(
                {
                    "error": "Book not found"
                },
                status=status.HTTP_404_NOT_FOUND
            )
        
        try:
            # Fetch member from database
            member = Member.objects.get(id=member_id)

        except Member.DoesNotExist:
            return Response(
                {"error": "Member not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        # # Check KYC status
        # if member.kyc_status != 'approved':
        #     return Response(
        #         {
        #             "error":"Member KYC is not approved. Book cannot be issued."
        #         },
        #         status=status.HTTP_400_BAD_REQUEST
        #     )

        # Check if book is available
        if book.available_copies <= 0:

            return Response(
                {
                    "error": "Book is not available"
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        # Validate incoming request data
        serializer = self.get_serializer(
            data=request.data
        )

        serializer.is_valid(
            raise_exception=True
        )

        # Save IssueBook record
        serializer.save()

        # Reduce available copies by 1
        book.available_copies -= 1

        # Save updated book data
        book.save()

        return Response(
            {
                "message": "Book issued successfully",
                "data": serializer.data
            },
            status=status.HTTP_201_CREATED
        )
    
class ReturnBookView(APIView):
    # Only Admin or Librarian can return books
    permission_classes = []

    def post(self, request, issue_id):

        try:
            issue = IssueBook.objects.get(id=issue_id)

        except IssueBook.DoesNotExist:

            return Response(
                {"error": "Issue record not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        # Prevent returning twice
        if issue.status == 'returned':

            return Response(
                {"error": "Book already returned"},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Get today's date
        today = date.today()

        # Mark book as returned
        issue.status = 'returned'
        
        # Save actual return date
        issue.return_date = today

        # Default fine amount
        fine_amount = 0

        # Check if the book is returned after due date
        if today > issue.due_date:

            # Calculate number of late days
            overdue_days = (today - issue.due_date).days

            # Fine rate per day (Rs. 5)
            fine_per_day = 5

            # Calculate total fine
            fine_amount = overdue_days * fine_per_day

        # Save fine amount
        issue.fine_amount = fine_amount
        issue.save()

        # Increase available copies
        book = issue.book
        book.available_copies += 1
        book.save()

        return Response(
            {"message": "Book returned successfully",
            "fine_amount": issue.fine_amount
            },
            status=status.HTTP_200_OK
        )
    

# New view to list all issued books
class IssueBookListView(generics.ListAPIView):

    queryset = IssueBook.objects.all()
    serializer_class = IssueBookSerializer

class OverdueBooksView(generics.ListAPIView):

    # Convert data to JSON
    serializer_class = IssueBookSerializer

    def get_queryset(self):

        # Return books that:
        # 1. Are still issued
        # 2. Due date has already passed

        return IssueBook.objects.filter(
            status='issued',
            due_date__lt=date.today()
        )
    
# Show recently issued books

class RecentTransactionsView(generics.ListAPIView):

    # Convert records to JSON
    serializer_class = IssueBookSerializer

    def get_queryset(self):

        # Order by latest issue date first
        # [:10] means only 10 records

        return IssueBook.objects.order_by(
            '-issue_date'
        )[:10]
    
class SendReminderView(APIView):

    def post(self, request):

        result = send_overdue_reminders()

        return Response({
            "message": result
        })
    


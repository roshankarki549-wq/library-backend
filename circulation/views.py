from datetime import date, timedelta
from urllib import request

# Allow Admin and Librarian users
from accounts.permissions import IsAdminOrLibrarian, IsStudent

from rest_framework.views import APIView, View
from rest_framework import generics
from rest_framework import status
from rest_framework.response import Response

from books.models import Book

from .models import IssueBook, User
from .serializers import BorrowRequestSerializer, IssueBookSerializer, DirectIssueSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from .reminders import send_overdue_reminders


class BorrowRequestView(generics.CreateAPIView):
    
    # Only logged-in users can borrow books
    permission_classes = [IsAuthenticated, IsStudent]

    # Serializer used for validation and saving
    serializer_class = BorrowRequestSerializer

    def create(self, request, *args, **kwargs):

        # Get book ID from request data
        book_id = request.data.get('book')

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
        
        # try:
        #     # Fetch member from database
        #     member = Member.objects.get(id=member_id)

        # except Member.DoesNotExist:
        #     return Response(
        #         {"error": "Member not found"},
        #         status=status.HTTP_404_NOT_FOUND
        #     )

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

        # Check if this student already has this book in pending or issued status
        existing_request = IssueBook.objects.filter(
            member=request.user,
            book=book,
            status__in=["pending", "issued"]
        ).exists()

        if existing_request:
            return Response(
                {
                    "error": "You already have a pending or issued request for this book."
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
        serializer.save(member=request.user)

        return Response(
            {
                "message": "Borrow request submitted successfully",
                "data": serializer.data
            },
            status=status.HTTP_201_CREATED
        )
    
class ApproveBorrowRequestView(APIView):
    # Approve a student's borrow request.
    # Only Admins and Librarians can approve requests.

    # Restrict access
    permission_classes = [IsAdminOrLibrarian]

    def post(self, request, issue_id):

        try:
            # Find the borrow request
            issue = IssueBook.objects.get(id=issue_id)

        except IssueBook.DoesNotExist:

            return Response(
                {
                    "error": "Borrow request not found."
                },
                status=status.HTTP_404_NOT_FOUND
            )

        # Prevent approving the same request twice
        if issue.status != "pending":

            return Response(
                {
                    "error": "This request has already been processed."
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        # Check whether copies are still available
        if issue.book.available_copies <= 0:

            return Response(
                {
                    "error": "No copies available."
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        # Approve the request
        issue.status = "issued"

        # Book issued today
        issue.issue_date = date.today()

        # Student must return within 14 days
        issue.due_date = date.today() + timedelta(days=14)

        issue.save()

        # Reduce available copies
        book = issue.book
        book.available_copies -= 1
        book.save()

        return Response(
            {
                "message": "Borrow request approved successfully."
            },
            status=status.HTTP_200_OK
        )
    
class RejectBorrowRequestView(APIView):
    """
    Reject a borrow request.

    Only Admins and Librarians can reject requests.
    """

    # Only Admin and Librarian are allowed
    permission_classes = [IsAdminOrLibrarian]

    def post(self, request, issue_id):

        try:
            # Find the borrow request
            issue = IssueBook.objects.get(id=issue_id)

        except IssueBook.DoesNotExist:

            return Response(
                {
                    "error": "Borrow request not found."
                },
                status=status.HTTP_404_NOT_FOUND
            )

        # Request has already been processed
        if issue.status != "pending":

            return Response(
                {
                    "error": "This request has already been processed."
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        # Reject the request
        issue.status = "rejected"

        # Save changes
        issue.save()

        return Response(
            {
                "message": "Borrow request rejected successfully."
            },
            status=status.HTTP_200_OK
        )
    
class DirectIssueView(generics.CreateAPIView):

    # Only admin/librarian can directly issue books
    permission_classes = [IsAdminOrLibrarian]

    serializer_class = DirectIssueSerializer

    def create(self, request, *args, **kwargs):

        book_id = request.data.get("book")
        member_id = request.data.get("member")

        # Check book
        try:
            book = Book.objects.get(id=book_id)

        except Book.DoesNotExist:
            return Response(
                {
                    "error": "Book not found"
                },
                status=status.HTTP_404_NOT_FOUND
            )

        # Check member
        try:
            member = User.objects.get(id=member_id)

        except User.DoesNotExist:
            return Response(
                {
                    "error": "Member not found"
                },
                status=status.HTTP_404_NOT_FOUND
            )

        # Only students can borrow books
        if member.role != "student":
            return Response(
                {
                    "error": "Books can only be issued to students."
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        # Book availability
        if book.available_copies <= 0:
            return Response(
                {
                    "error": "Book is not available."
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        # Prevent duplicate issue
        if IssueBook.objects.filter(
            member=member,
            book=book,
            status="issued"
        ).exists():
            return Response(
                {
                    "error": "Student already has this book."
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        # Create issue record
        issue = IssueBook.objects.create(
            book=book,
            member=member,
            status="issued"
        )

        # Reduce available copies
        book.available_copies -= 1
        book.save()

        return Response(
            {
                "message": "Book issued successfully.",
                "data": IssueBookSerializer(issue).data
            },
            status=status.HTTP_201_CREATED
        )
    
class ReturnBookView(APIView):

    """
    Return an issued book.
    Only Admins and Librarians can return books.
    """
    permission_classes = [IsAdminOrLibrarian]

    def post(self, request, issue_id):

        try:
            # Find the issue record
            issue = IssueBook.objects.get(id=issue_id)

        except IssueBook.DoesNotExist:
            return Response(
                {
                    "error": "Issue record not found."
                },
                status=status.HTTP_404_NOT_FOUND
            )

        # Only issued books can be returned
        if issue.status != "issued":
            return Response(
                {
                    "error": "Only issued books can be returned."
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        # Today's date
        today = date.today()

        # Update issue record
        issue.status = "returned"
        issue.return_date = today

        # Fine Calculation
        fine = 0

        # Check if returned after due date
        if today > issue.due_date:

            # Number of late days
            overdue_days = (today - issue.due_date).days

            # Fine = Rs. 5 per day
            fine = overdue_days * 5

        issue.fine_amount = fine

        issue.save()

        # Increase available copies
        book = issue.book
        book.available_copies += 1
        book.save()

        return Response(
            {
                "message": "Book returned successfully.",
                "fine_amount": fine
            },
            status=status.HTTP_200_OK
        )

class MyBorrowHistoryView(generics.ListAPIView):

    # Student can view only their own borrow history.
    serializer_class = IssueBookSerializer

    permission_classes = [IsStudent]

    def get_queryset(self):

        return IssueBook.objects.filter(
            member=self.request.user
        ).order_by("-request_date")
    
class PendingBorrowRequestView(generics.ListAPIView):
    #View all pending borrow requests.

    serializer_class = IssueBookSerializer

    permission_classes = [IsAdminOrLibrarian]

    def get_queryset(self):

        return IssueBook.objects.filter(
            status="pending"
        ).order_by("request_date")
    
class IssuedBooksView(generics.ListAPIView):
    # View all issued books.

    serializer_class = IssueBookSerializer

    permission_classes = [IsAdminOrLibrarian]

    def get_queryset(self):

        return IssueBook.objects.filter(
            status="issued"
        ).order_by("-issue_date")

class OverdueBooksView(generics.ListAPIView):

    # View all overdue books.
    serializer_class = IssueBookSerializer

    permission_classes = [IsAdminOrLibrarian]

    def get_queryset(self):

        return IssueBook.objects.filter(
            status="issued",
            due_date__lt=date.today()
        ).order_by("due_date")
    
# Show recently issued books
class RecentTransactionsView(generics.ListAPIView):

    # Show latest circulation activities.

    serializer_class = IssueBookSerializer
    permission_classes = [IsAdminOrLibrarian]

    def get_queryset(self):

        return IssueBook.objects.order_by(
            "-request_date"
        )[:10]
    
class SendReminderView(APIView):

    def post(self, request):

        result = send_overdue_reminders()

        return Response({
            "message": result
        })
    


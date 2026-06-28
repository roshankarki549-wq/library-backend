from django.db import models
from books.models import Book
from accounts.models import User

class IssueBook(models.Model):

    # Possible states of a borrow request
    STATUS_CHOICES = (
        ('pending', 'Pending'),    # Student requested book
        ('issued', 'Issued'),      # Librarian approved request
        ('returned', 'Returned'),  # Book returned
        ('rejected', 'Rejected'),  # Request rejected
    )

    # Book being requested/issued
    book = models.ForeignKey(
        Book,
        on_delete=models.CASCADE
    )

    # Student who requested the book
    # We use User because students are stored in accounts app
    member = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    # Date when student submitted borrow request
    request_date = models.DateField(
        auto_now_add=True
    )

    # Date when librarian approved and issued the book
    # Empty while request is pending
    issue_date = models.DateField(
        null=True,
        blank=True
    )

    # Expected return date
    # Set when book is issued
    due_date = models.DateField(
        null=True,
        blank=True
    )

    # Actual date when student returned the book
    return_date = models.DateField(
        null=True,
        blank=True
    )

    # Current request status
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending'
    )

    # Fine charged for late return
    fine_amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0
    )

    def __str__(self):
        return f"{self.member.username} - {self.book.title}"

    class Meta:
        # Always show oldest records first
        ordering = ['id']
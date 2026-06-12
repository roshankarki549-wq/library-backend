from django.db import models
from datetime import date, timedelta

# Import Book and Member models
from books.models import Book
from members.models import Member

class IssueBook(models.Model):
    # Choices for book status
    STATUS_CHOICES = (
        ('issued', 'Issued'),
        ('returned', 'Returned')
    )

    # Which book is being issued
    book = models.ForeignKey(Book,on_delete=models.CASCADE)

    # Which member borrowed the book
    member = models.ForeignKey(Member,on_delete=models.CASCADE)

    # Date when book is issued
    issue_date = models.DateField(default=date.today)

    # Expected return date
    due_date = models.DateField()

    # Actual return date
    return_date = models.DateField(
        null=True,
        blank=True
    )

    # Current status of book issue
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='issued'
    )

     # Fine amount in rupees
    fine_amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0
    )

    def __str__(self):
        return f"{self.member.full_name} - {self.book.title}"
    
    def save(self, *args, **kwargs):
        if not self.due_date:
            self.due_date = self.issue_date + timedelta(days=14)

        super().save(*args, **kwargs)

    class Meta:
        ordering = ["id"] 
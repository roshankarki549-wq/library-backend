from datetime import date

from django.core.mail import send_mail

from .models import IssueBook


def send_overdue_reminders():

    # Find overdue books that are not returned

    overdue_books = IssueBook.objects.filter(
        status='issued',
        due_date__lt=date.today()
    )

    for issue in overdue_books:

        send_mail(

            subject='Library Book Overdue',

            message=f"""
Dear {issue.member.full_name},

The book "{issue.book.title}" is overdue.

Due Date: {issue.due_date}

Please return it as soon as possible.

Library Management System
""",

            from_email='roshankarki549@gmail.com',

            recipient_list=[issue.member.email],

            fail_silently=False
        )

    return f"{overdue_books.count()} reminder(s) sent."
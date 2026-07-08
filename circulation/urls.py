from django.urls import path

from .views import (BorrowRequestView, IssuedBooksView, MyBorrowHistoryView, OverdueBooksView, PendingBorrowRequestView, RecentTransactionsView, ReturnBookView, SendReminderView,
ApproveBorrowRequestView, RejectBorrowRequestView,DirectIssueView)

urlpatterns = [
    # Issue a book
    path('borrow/',BorrowRequestView.as_view(),name='borrow-book'),
    path("approve/<int:issue_id>/",ApproveBorrowRequestView.as_view(),name="approve-borrow",),
    path("issue-direct/",DirectIssueView.as_view(),name="direct-issue"),
    path('return/<int:issue_id>/',ReturnBookView.as_view(),name='return-book'),
    path("reject/<int:issue_id>/",RejectBorrowRequestView.as_view(),name="reject-borrow",),
    path("my-books/",MyBorrowHistoryView.as_view(),name="my-books",),
    path("pending/",PendingBorrowRequestView.as_view(),name="pending-borrow-requests",),
    path("issued/",IssuedBooksView.as_view(),name="issued-books",),
    path('overdue/',OverdueBooksView.as_view(),name="overdue-books"),
    path('recent-transactions/',RecentTransactionsView.as_view(),name='recent-transactions'),
    
    path('send-reminders/', SendReminderView.as_view()),

]
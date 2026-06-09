from django.urls import path

from .views import IssueBookCreateView, OverdueBooksView, RecentTransactionsView, ReturnBookView,IssueBookListView, SendReminderView

urlpatterns = [
    # Issue a book
    path('issue/', IssueBookCreateView.as_view(), name='issue-book'),
    path('issues/',IssueBookListView.as_view(),name='issue-list'),
    path('return/<int:issue_id>/',ReturnBookView.as_view(),name='return-book'),
    path('overdue-books/',OverdueBooksView.as_view(),name='overdue-books'),
    path('recent-transactions/',RecentTransactionsView.as_view(),name='recent-transactions'),
    path('send-reminders/', SendReminderView.as_view()),

]
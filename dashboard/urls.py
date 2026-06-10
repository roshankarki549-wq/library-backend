from django.urls import path
from .views import (CategoryDistributionView, DashboardStatsView, IssueReturnChartView,NotificationsView, PopularBooksView, RecentIssuesView)

urlpatterns = [
    path('stats/',DashboardStatsView.as_view(),name='dashboard-stats'),
    path('recent-issues/',RecentIssuesView.as_view()),
    path('popular-books/',PopularBooksView.as_view()),
    path('notifications/',NotificationsView.as_view(),name='notifications'),
    path('category-distribution/',CategoryDistributionView.as_view()),
    path('issue-return-chart/',IssueReturnChartView.as_view()),

]
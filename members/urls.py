from django.urls import path
from .views import MemberListCreateView, MemberDetailView
from .views import (PendingKYCView, ApproveKYCView, RejectKYCView)


urlpatterns = [
    path('', MemberListCreateView.as_view()),
    path('<int:pk>/', MemberDetailView.as_view()),
     # View all pending KYC requests
    path('pending-kyc/',PendingKYCView.as_view()),

    # Approve member KYC
    path('approve-kyc/<int:member_id>/',ApproveKYCView.as_view()),

    # Reject member KYC
    path('reject-kyc/<int:member_id>/',RejectKYCView.as_view()),
]
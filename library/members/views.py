from rest_framework import generics, filters
from rest_framework.parsers import (MultiPartParser, FormParser)
from rest_framework.views import APIView
from rest_framework.response import Response

from .models import Member
from .serializers import MemberSerializer

class MemberListCreateView(generics.ListCreateAPIView):
    parser_classes = (MultiPartParser, FormParser) # To handle image uploads
    queryset = Member.objects.all()
    serializer_class = MemberSerializer

    filter_backends = [filters.SearchFilter]

    search_fields = [
        'full_name',
        'email',
        'department',
        'roll_no'
    ]

class MemberDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Member.objects.all()
    serializer_class = MemberSerializer

class PendingKYCView(APIView):

    def get(self, request):

        # Get all members whose KYC has not yet been reviewed
        members = Member.objects.filter(
            kyc_status='pending'
        )

        data = []

        for member in members:
            data.append({
                # Member ID
                "id": member.id,

                # Member Name
                "full_name": member.full_name,

                # Member Email
                "email": member.email,

                # Profile Photo URL
                "photo":
                member.photo.url
                if member.photo
                else None,

                # KYC Document URL
                "id_proof":
                member.id_proof.url
                if member.id_proof
                else None,

                # Current Status
                "kyc_status":
                member.kyc_status

            })

        return Response(data)
    
class ApproveKYCView(APIView):
    def post(self, request, member_id):

        try:

            # Find member by ID
            member = Member.objects.get(
                id=member_id
            )

        except Member.DoesNotExist:

            return Response(
                {
                    "error":
                    "Member not found"
                },
                status=404
            )

        # Mark KYC as approved
        member.kyc_status = 'approved'
        member.save()
        return Response({
            "message": "KYC approved successfully"
        })
    
class RejectKYCView(APIView):

    def post(self, request, member_id):

        try:
            # Find member
            member = Member.objects.get(
                id=member_id
            )

        except Member.DoesNotExist:
            return Response(
                {
                    "error":"Member not found"
                },
                status=404
            )

        # Reject KYC
        member.kyc_status = 'rejected'
        member.save()
        return Response({
            "message": "KYC rejected successfully"
        })
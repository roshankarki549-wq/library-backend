from rest_framework import serializers
from .models import IssueBook

# Converts IssueBook objects <-> JSON
class IssueBookSerializer(serializers.ModelSerializer):

    class Meta:
        model = IssueBook

        # Include all model fields
        fields = '__all__'
        read_only_fields = ['issue_date', 'due_date']
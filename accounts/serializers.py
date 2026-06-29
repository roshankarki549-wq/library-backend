from rest_framework import serializers
from django.contrib.auth import authenticate
from .models import User, StudentProfile

class RegisterSerializer(serializers.ModelSerializer):

    password = serializers.CharField(write_only=True)

    # Student fields
    roll_no = serializers.CharField(required=False)
    department = serializers.CharField(required=False)
    id_proof = serializers.FileField(required=False)

    class Meta:
        model = User

        fields = [
            "id",
            "username",
            "email",
            "password",
            "role",
            "first_name",
            "last_name",
            "phone",
            "address",
            "profile_picture",

            # StudentProfile fields
            "roll_no",
            "department",
            "id_proof",
        ]

    def create(self, validated_data):

        # Remove student profile fields
        roll_no = validated_data.pop("roll_no", None)
        department = validated_data.pop("department", None)
        id_proof = validated_data.pop("id_proof", None)

        # Create user
        user = User.objects.create_user(**validated_data)
        
        # Create student profile if the user is a student
        if user.role == 'student':
            StudentProfile.objects.create(
                user=user,
                roll_no=roll_no,
                department=department,
                id_proof=id_proof
            )
        return user
    

def validate(self, attrs):

    role = attrs.get("role")

    if role == "student":
        if not attrs.get("roll_no"):
            raise serializers.ValidationError({
                "roll_no": "This field is required."
            })

        if not attrs.get("department"):
            raise serializers.ValidationError({
                "department": "This field is required."
            })
    return attrs
   
class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        
        fields = (
            'id',
            'username',
            'email',
            'role'
        )

        read_only_fields = (
            'id',
        )

class LoginSerializer(serializers.Serializer):

    # User enters email
    email = serializers.EmailField()

    # User enters password
    password = serializers.CharField(
        write_only=True
    )

    def validate(self, attrs):

        email = attrs.get("email")
        password = attrs.get("password")

        # Find user by email
        try:
            user = User.objects.get(email=email)

        except User.DoesNotExist:
            raise serializers.ValidationError(
                "Invalid email or password."
            )

        # Authenticate using username internally
        user = authenticate(
            username=user.username,
            password=password
        )

        if user is None:
            raise serializers.ValidationError(
                "Invalid email or password."
            )

        attrs["user"] = user

        return attrs
    
class GoogleLoginSerializer(serializers.Serializer):
    id_token = serializers.CharField()
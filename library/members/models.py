from django.db import models

class Member(models.Model):
    # KYC verification status choices
    KYC_STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected')
    )
    full_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20)
    address = models.TextField(default="Not Provided")

    # Profile photo
    photo = models.ImageField(
        upload_to='members/',
        blank=True,
        null=True
    )

    # Citizenship / Student ID / Passport
    id_proof = models.FileField(
        upload_to='kyc/',
        blank=True,
        null=True
    )

     # Current KYC status
    kyc_status = models.CharField(
        max_length=20,
        choices=KYC_STATUS_CHOICES,
        default='pending'
    )

    # Registration date
    created_at = models.DateField(
        auto_now_add=True
    )

    department = models.CharField(max_length=100)
    roll_no = models.CharField(max_length=50)

    joined_at = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.full_name
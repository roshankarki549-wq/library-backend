from django.db import models

class Book(models.Model):
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)

    category = models.CharField(max_length=100)

    isbn = models.CharField(
        max_length=20,
        unique=True
    )

    total_copies = models.IntegerField()

    available_copies = models.IntegerField()
    
    # Book cover image
    cover_image = models.URLField(blank=True, null=True)

    created_at = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.title
    
    class Meta:
        ordering = ["id"] 
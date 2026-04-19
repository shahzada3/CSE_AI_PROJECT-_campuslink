from django.db import models
from accounts.models import User


class SharedFile(models.Model):
    FILE_TYPES = [
        ('pdf', 'PDF'),
        ('doc', 'Document'),
        ('img', 'Image'),
        ('other', 'Other'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='uploaded_files')
    title = models.CharField(max_length=200)
    file = models.FileField(upload_to='uploads/')
    description = models.TextField(blank=True)
    file_type = models.CharField(max_length=10, choices=FILE_TYPES, default='other')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    download_count = models.IntegerField(default=0)

    class Meta:
        ordering = ['-uploaded_at']

    def __str__(self):
        return self.title

    def filename(self):
        return self.file.name.split('/')[-1]
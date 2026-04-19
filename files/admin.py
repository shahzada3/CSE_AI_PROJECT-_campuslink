from django.contrib import admin
from .models import SharedFile

@admin.register(SharedFile)
class SharedFileAdmin(admin.ModelAdmin):
    list_display = ['title', 'user', 'file_type', 'uploaded_at', 'download_count']
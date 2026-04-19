from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    bio = models.TextField(blank=True)
    profile_pic = models.ImageField(upload_to='profiles/', null=True, blank=True)
    skills = models.CharField(max_length=500, blank=True)
    college = models.CharField(max_length=200, blank=True)
    branch = models.CharField(max_length=200, blank=True)
    year = models.CharField(max_length=10, blank=True)
    github = models.URLField(blank=True)
    linkedin = models.URLField(blank=True)

    def __str__(self):
        return self.username

    def get_profile_pic_url(self):
        if self.profile_pic:
            return self.profile_pic.url
        return None

    def skills_list(self):
        if not self.skills:
            return []
        return [s.strip() for s in self.skills.split(',') if s.strip()]

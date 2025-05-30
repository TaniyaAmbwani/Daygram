from django.contrib.auth.models import AbstractUser
from django.db import models

# Custom User Model
class CustomUser(AbstractUser):
    GENDER_CHOICES = [
        ('Male', 'Male'),
        ('Female', 'Female'),
        ('Other', 'Other'),
    ]
    
    name = models.CharField(max_length=100)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, null=True, blank=True)
    mobile = models.CharField(max_length=15, null=True, blank=True)
    profile_pic = models.ImageField(upload_to='profile_pics/', default='profile_pics/default.jpg')
    
    # For followers and following
    followers = models.ManyToManyField('self', symmetrical=False, related_name='following', blank=True)
    
    last_login = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return self.username

    # To get followers count
    def get_followers_count(self):
        return self.followers.count()

    # To get following count
    def get_following_count(self):
        return self.following.count()

# Post Model
class Post(models.Model):
    user_profile = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True, blank=True)
    caption = models.TextField(null=True, blank=True)  # Made optional (null=True and blank=True)
    image = models.ImageField(upload_to='uploads/', null=True, blank=True)  # Image upload
    video = models.FileField(upload_to='videos/', null=True, blank=True)    # Video upload
    category = models.CharField(max_length=100, null=True, blank=True)  # Made optional
    created_at = models.DateTimeField(auto_now_add=True)
    is_approved = models.BooleanField(default=False)  # New field
    
    # For saving posts
    saved_by = models.ManyToManyField(CustomUser, related_name='saved_posts', blank=True)

    def __str__(self):
        return self.caption or "No Caption"

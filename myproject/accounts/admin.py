from django.contrib import admin
from .models import *

admin.site.register(CustomUser)


class PostAdmin(admin.ModelAdmin):
    list_display = ('user_profile', 'created_at', 'is_approved')
    list_filter = ('is_approved',)
    actions = ['approve_posts']

    def approve_posts(self, request, queryset):
        queryset.update(is_approved=True)
    approve_posts.short_description = "Mark selected posts as approved"

admin.site.register(Post, PostAdmin)
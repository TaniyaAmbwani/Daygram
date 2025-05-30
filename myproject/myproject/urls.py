"""
URL configuration for myproject project.

The urlpatterns list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from accounts.views import *
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.views import LogoutView  # ✅ Correct import


urlpatterns = [
    path('', home , name = "home"),  # Includes the URLs of the accounts app
    path('register/', register , name = "register"),  
    path('login/', login_page , name = "login_page"),  
    path('chatbot/', chatbot, name = "chatbot"),
    path('post/', post, name = "post"),
    path('search/', search, name = "search"),
    path('games/' , games, name = "games"),
    path('profile/<int:id>/', profile, name='profile'),  # Profile page needs an ID
    path("follow/", follow_unfollow, name="follow_unfollow"),
    path("toggle_follow/<int:user_id>/", toggle_follow, name="toggle_follow"),
    path('profile/',profile, name='profile'),
    path('post/blog/', blog, name='blog'),
    path('run_skychaser/', run_skychaser, name='run_skychaser'),
    path('run_fastLane/', run_fastLane, name='run_fastLane'),
    path('run_attackAliens/', run_attackAliens, name='run_attackAliens'),
    path('hissHunt/', hissHunt, name='hissHunt'),
    path('like/<int:post_id>/', like_post, name='like_post'),
    path('comment/<int:post_id>/', add_comment, name='add_comment'),
    path('save/<int:post_id>/', save_post, name='save_post'),
    path('edit-profile/', edit_profile, name='edit_profile'),
    path('logout/', logout, name='logout'),  # ✅ Use custom logout view
    path('admin/', admin.site.urls),  # Admin site
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
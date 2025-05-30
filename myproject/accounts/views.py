from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login
from django.db.models import Q
from django.contrib import messages
from django.contrib.auth.hashers import make_password
from django.conf import settings
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from .models import *
import os
import subprocess
from .forms import *
from django.http import JsonResponse
from django.contrib.auth.forms import PasswordChangeForm
from django.urls import reverse  # ✅ Import reverse
from django.contrib.auth import update_session_auth_hash


@login_required(login_url='/login/')
def home(request):
    user = request.user

    # Get the users the current user is following
    following_users = user.following.all()

    # Get the posts from users the current user is following, and their own posts
    posts = Post.objects.filter(
        Q(user_profile__in=following_users) | Q(user_profile=user)
    )

    # Also, make sure the user's posts appear in the feed of their followers
    follower_users = user.followers.all()
    posts |= Post.objects.filter(user_profile__in=follower_users)

    # Order posts by creation date, newest first
    posts = posts.distinct().order_by('-created_at')  # Use distinct to avoid duplicates

    context = {
        'posts': posts
    }
    return render(request, 'home.html', context)

def login_page(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        if not CustomUser.objects.filter(username=username).exists():
            messages.error(request, "Invalid username")
            return render(request, "login.html")

        user = authenticate(username=username, password=password)
        if user is None:
            messages.error(request, 'Invalid Password')
            return redirect('/login/')
        
        else:
            login(request, user)
            return redirect('home')

    return render(request, 'login.html')


def logout(request):
    return redirect('/login/')  # ✅ Redirect to the correct login page


def register(request):
    if request.method == "POST":
        print("Register view triggered")  # Debugging line
        
        username = request.POST["username"]
        email = request.POST["email"]
        password = request.POST["password"]

        if CustomUser.objects.filter(username=username).exists():
            messages.error(request, "Username already exists!")
            return redirect("register")

        user = CustomUser.objects.create_user(username=username, email=email, password=password)
        user.save()
        
        print(f"User {username} created successfully")  # Debugging line

        messages.success(request, "Account created successfully!")
        return redirect("/login/")

    return render(request, "register.html")


def chatbot(request):
    return render(request, "chatbot.html")


@login_required
def post(request):
    if request.method == 'POST':
        caption = request.POST.get('caption')
        category = request.POST.get('category')
        media = request.FILES.get('media')

        image = None
        video = None

        if media:
            if media.content_type.startswith('image'):
                image = media
            elif media.content_type.startswith('video'):
                video = media

        # Save post as unapproved
        post = Post(
            user_profile=request.user,
            caption=caption,
            category=category,
            image=image,
            video=video,
            is_approved=False
        )
        post.save()

        # ✅ Show success alert
        messages.success(request, "Your post has been submitted and is awaiting admin approval.")
        return redirect('post')  # Reload the same page to show the message

    posts = Post.objects.filter(is_approved=True).order_by('-created_at')
    return render(request, 'post.html', {'posts': posts})

@login_required
def follow_unfollow(request):
    if request.method == "POST":
        user_id = request.POST.get("user_id")
        user_to_follow = get_object_or_404(User, id=user_id)
        profile = request.user.profile  # Assuming profile is linked to User via OneToOneField

        if user_to_follow in profile.following.all():
            profile.following.remove(user_to_follow)
            followed = False
        else:
            profile.following.add(user_to_follow)
            followed = True

        followers_count = user_to_follow.profile.followers.count()
        following_count = profile.following.count()

        return JsonResponse({
            "followed": followed,
            "followers_count": followers_count,
            "following_count": following_count
        })

    return JsonResponse({"error": "Invalid request"}, status=400)

@login_required
def toggle_follow(request, user_id):
    if request.method == "POST":
        user_to_follow = get_object_or_404(CustomUser, id=user_id)
        current_user = request.user

        if user_to_follow in current_user.following.all():
            current_user.following.remove(user_to_follow)
            followed = False
        else:
            current_user.following.add(user_to_follow)
            followed = True

        return JsonResponse({
            "followed": followed,
            "followers_count": user_to_follow.get_followers_count(),
            "following_count": user_to_follow.get_following_count(),
        })
    return JsonResponse({"error": "Invalid request"}, status=400)

@login_required
def profile(request, id):
    # Get the current user's profile (assuming id is used to fetch the profile)
    user_profile = get_object_or_404(CustomUser, id=id)
    
    # Get followers and following count
    followers_count = user_profile.followers.count()  # Assuming 'followers' is a related field
    following_count = user_profile.following.count()  # Assuming 'following' is a related field
    
    # Get the user's posts
    user_posts = Post.objects.filter(user_profile=user_profile)
    
    # Get the user's saved posts
    saved_posts = user_profile.saved_posts.all()  # This should correctly return the posts the user saved

    # Pass all context data
    context = {
        'user_profile': user_profile,
        'followers_count': followers_count,
        'following_count': following_count,
        'user_posts': user_posts,
        'saved_posts': saved_posts,
    }
    
    # Render the profile template with the context
    return render(request, 'profile.html', context)



def games(request):
    return render(request, 'games.html')

def blog(request):
    if request.method == 'POST':
        caption = request.POST.get("Caption")  # Capturing the caption input

        # Check if caption is provided
        if not caption:
            messages.error(request, "Caption is required!")
            return render(request, "blog.html")
        
        # Create the post and associate it with the logged-in user
        Post.objects.create(
            user_profile=request.user,  # Associate with current user
            caption=caption
        )

        messages.success(request, "Blog posted successfully!")
        return redirect("home")

    return render(request, 'blog.html')


def search(request):
    query = request.GET.get('query', '').strip()
    category = request.GET.get('category', '')

    if category == "username":
        users = CustomUser.objects.filter(username__icontains=query)
        if users.count() == 1:  # If only one user found, redirect directly
            return redirect('profile', id=users.first().id)
    else:
        users = None

    posts = Post.objects.filter(caption__icontains=query) if query else []

    return render(request, 'search.html', {'posts': posts, 'query': query, 'category': category, 'users': users})


def run_skychaser(request):
    game_path = os.path.join(settings.BASE_DIR, 'accounts', 'static', 'games', 'skychaser.py')
    subprocess.Popen(['python', game_path])  # Runs the game in the background
    return HttpResponse(status=204)  # No content (prevents page from opening)


def run_fastLane(request):
    game_path = os.path.join(settings.BASE_DIR, 'accounts', 'static', 'games', 'fast_Lane.py')

    try:
        subprocess.Popen(['python', game_path])  # Corrected syntax
    except Exception as e:
        return HttpResponse(f"Error launching Fast Lane: {str(e)}", status=500)

    return HttpResponse(status=204)  # No intermediate page opens


def run_attackAliens(request):
    game_path = os.path.join(settings.BASE_DIR, 'accounts', 'static', 'games', 'attackAliens.py')
    subprocess.Popen(['python', game_path])
    return HttpResponse(status=204)


def hissHunt(request):
    return render(request, "hissHunt.html")

@login_required
def edit_profile(request):
    user = request.user
    if request.method == "POST":
        form = ProfileUpdateForm(request.POST, request.FILES, instance=user)
        password_form = PasswordChangeForm(user, request.POST)

        if form.is_valid():
            form.save()

        if password_form.is_valid():
            password_form.save()
            update_session_auth_hash(request, user)  # ✅ Keep user logged in with new password
            messages.success(request, "Your password was successfully updated!")
            return redirect(reverse('profile', args=[user.id]))
        else:
            for field, errors in password_form.errors.items():
                for error in errors:
                    messages.error(request, f"{field}: {error}")  # ✅ Show exact errors

    else:
        form = ProfileUpdateForm(instance=user)
        password_form = PasswordChangeForm(user)

    return render(request, 'edit_profile.html', {'form': form, 'password_form': password_form})

def like_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    
    if request.method == "POST":
        post.likes.add(request.user)  # Ensure your model supports this
        new_like_count = post.likes.count()
        
        return JsonResponse({"success": True, "likes": new_like_count})
    
    return JsonResponse({"success": False})

def add_comment(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if request.method == "POST":
        text = request.POST.get("text", "")
        comment = Comment.objects.create(user=request.user, post=post, text=text)
        return JsonResponse({"user": request.user.username, "text": comment.text})



def save_post(request, post_id):
    if request.user.is_authenticated:
        post = get_object_or_404(Post, id=post_id)
        user_profile = request.user.profile  # Assuming you have a user profile model

        # Check if the post is already saved by the user
        if post.saved_by.filter(id=user_profile.id).exists():
            # If the user has already saved the post, unsave it
            post.saved_by.remove(user_profile)
            saved = False
        else:
            # If the user hasn't saved the post, save it
            post.saved_by.add(user_profile)
            saved = True

        # Return a JSON response to notify the frontend
        return JsonResponse({'saved': saved})
    else:
        return JsonResponse({'error': 'User not authenticated'}, status=403)


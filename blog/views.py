from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from .models import Post, Category, Tag, Comment, Like, UserProfile
from .forms import RegisterForm, UserUpdateForm, ProfileUpdateForm, PostForm, CommentForm
from django.http import HttpResponse
from django.views.decorators.http import require_GET
from django.http import HttpResponse, JsonResponse
from django.utils import timezone
from django.conf import settings
import traceback


# ----------- AUTH VIEWS -----------

def register_view(request):
    if request.user.is_authenticated:
        return redirect('home')
    form = RegisterForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, f'Welcome to StitchTales, {user.first_name}! 🧶')
            return redirect('home')
    return render(request, 'auth/register.html', {'form': form})


def login_view(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, f'Welcome back, {user.first_name}! 🧶')
            return redirect('home')
        else:
            messages.error(request, 'Invalid username or password.')
    return render(request, 'auth/login.html')


@login_required
def logout_view(request):
    logout(request)
    messages.success(request, 'You have been logged out.')
    return redirect('home')


@login_required
def profile_view(request):
    profile, _ = UserProfile.objects.get_or_create(user=request.user)
    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, instance=request.user)
        profile_form = ProfileUpdateForm(request.POST, request.FILES, instance=profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Your profile has been updated!')
            return redirect('profile')
    else:
        user_form = UserUpdateForm(instance=request.user)
        profile_form = ProfileUpdateForm(instance=profile)
    return render(request, 'auth/profile.html', {
        'user_form': user_form,
        'profile_form': profile_form
    })


def author_detail(request, username):
    author = get_object_or_404(User, username=username)
    posts = Post.objects.filter(author=author, status='published')
    return render(request, 'auth/author_detail.html', {'author': author, 'posts': posts})


# ----------- BLOG VIEWS -----------

def home(request):
    posts = Post.objects.filter(status='published').select_related('author', 'category')
    categories = Category.objects.all()
    tags = Tag.objects.all()
    return render(request, 'blog/home.html', {
        'posts': posts,
        'categories': categories,
        'tags': tags,
    })


def post_detail(request, slug):
    post = get_object_or_404(Post, slug=slug, status='published')
    is_liked = False

    post.view_count += 1
    post.save(update_fields=['view_count'])

    if request.user.is_authenticated:
        is_liked = Like.objects.filter(post=post, user=request.user).exists()

    if request.method == 'POST' and request.user.is_authenticated:
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.save()
            messages.success(request, 'Comment added!')
            return redirect('post_detail', slug=slug)
    else:
        comment_form = CommentForm()

    # fetch comments AFTER potential save and redirect
    comments = post.comments.filter(is_approved=True)

    related_posts = Post.objects.filter(
        category=post.category, status='published'
    ).exclude(id=post.id)[:3]

    return render(request, 'blog/post_detail.html', {
        'post': post,
        'comments': comments,
        'comment_form': comment_form,
        'is_liked': is_liked,
        'related_posts': related_posts,
    })

def category_detail(request, slug):
    category = get_object_or_404(Category, slug=slug)
    posts = Post.objects.filter(category=category, status='published')
    return render(request, 'blog/category_detail.html', {'category': category, 'posts': posts})


def tag_detail(request, slug):
    tag = get_object_or_404(Tag, slug=slug)
    posts = Post.objects.filter(tags=tag, status='published')
    return render(request, 'blog/tag_detail.html', {'tag': tag, 'posts': posts})


def search_view(request):
    query = request.GET.get('q', '')
    posts = Post.objects.filter(status='published')
    if query:
        posts = posts.filter(title__icontains=query) | posts.filter(content__icontains=query)
    return render(request, 'blog/search.html', {'posts': posts, 'query': query})


# ----------- HTMX VIEWS -----------
@login_required
def like_post(request, slug):
    post = get_object_or_404(Post, slug=slug)
    like, created = Like.objects.get_or_create(post=post, user=request.user)
    if not created:
        like.delete()
        is_liked = False
    else:
        is_liked = True
    return render(request, 'partials/like_button.html', {
        'post': post,
        'is_liked': is_liked,
    })


# ----------- DASHBOARD -----------

@login_required
def dashboard(request):
    posts = Post.objects.filter(author=request.user).select_related('category').prefetch_related('tags')
    
    # Statistics
    total_posts = posts.count()
    published_posts = posts.filter(status='published').count()
    draft_posts = posts.filter(status='draft').count()
    total_views = sum(post.view_count for post in posts)
    total_comments = Comment.objects.filter(post__author=request.user).count()
    total_likes = Like.objects.filter(post__author=request.user).count()
    
    # Recent activity
    recent_comments = Comment.objects.filter(
        post__author=request.user
    ).select_related('post', 'author').order_by('-created_at')[:5]
    
    # Top performing posts
    top_posts = posts.filter(status='published').order_by('-view_count')[:5]
    
    return render(request, 'blog/dashboard.html', {
        'posts': posts.order_by('-created_at'),
        'total_posts': total_posts,
        'published_posts': published_posts,
        'draft_posts': draft_posts,
        'total_views': total_views,
        'total_comments': total_comments,
        'total_likes': total_likes,
        'recent_comments': recent_comments,
        'top_posts': top_posts,
    })


@login_required
def post_create(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            form.save_m2m()
            messages.success(request, 'Post created successfully!')
            return redirect('post_detail', slug=post.slug)
    else:
        form = PostForm()
    return render(request, 'blog/post_form.html', {'form': form, 'action': 'Create'})


@login_required
def post_edit(request, slug):
    post = get_object_or_404(Post, slug=slug, author=request.user)
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            form.save()
            messages.success(request, 'Post updated successfully!')
            return redirect('post_detail', slug=post.slug)
    else:
        form = PostForm(instance=post)
    return render(request, 'blog/post_form.html', {'form': form, 'action': 'Edit'})


@login_required
def post_delete(request, slug):
    post = get_object_or_404(Post, slug=slug, author=request.user)
    if request.method == 'POST':
        post.delete()
        messages.success(request, 'Post deleted.')
        return redirect('dashboard')
    return render(request, 'blog/post_confirm_delete.html', {'post': post})

#Adding robots.txt views


@require_GET
def robots_txt(request):
    lines=[
        "User-Agent:*",
        "Disallow:/admin/",
        "Disallow:/dashboard/",
        "Disallow:/profile/",
        "Allow:/",
        "",
        f"Sitemap:{request.scheme}://{request.get_host()}/sitemap.xml",
    ]
    return HttpResponse("\n".join(lines),content_type="text/plain")

def handler404(request,exception):
    return render(request,"404.html",status=404)


def handler500(request):
    return render(request,"500.html",status=500)


from django.http import JsonResponse
import os
from django.conf import settings

def test_cloudinary(request):
    cloudinary_status = {
        'cloud_name': os.getenv('CLOUDINARY_CLOUD_NAME', 'NOT SET'),
        'api_key_set': 'YES' if os.getenv('CLOUDINARY_API_KEY') else 'NO',
        'api_secret_set': 'YES' if os.getenv('CLOUDINARY_API_SECRET') else 'NO',
        'cloudinary_in_apps': 'cloudinary' in settings.INSTALLED_APPS,
        'storage_backend': getattr(settings, 'DEFAULT_FILE_STORAGE', 'NOT SET'),
        'debug': settings.DEBUG,
    }
    return JsonResponse(cloudinary_status)

from django.utils import timezone

@login_required
def test_upload(request):
    if request.method == 'POST' and request.FILES.get('test_image'):
        try:
            test_post = Post(
                title="Test Upload " + str(timezone.now()),
                content="Testing cloudinary upload",
                author=request.user,
                slug="test-upload-" + str(timezone.now().timestamp()),
                cover_image=request.FILES['test_image']
            )
            test_post.save()
            
            return JsonResponse({
                'success': True,
                'image_url': test_post.cover_image.url if test_post.cover_image else 'NO URL',
                'image_name': str(test_post.cover_image.name) if test_post.cover_image else 'NO NAME',
                'storage_backend': getattr(settings, 'DEFAULT_FILE_STORAGE', 'NOT SET')
            })
        except Exception as e:
            import traceback
            return JsonResponse({
                'success': False,
                'error': str(e),
                'traceback': traceback.format_exc()
            })
    
    from django.middleware.csrf import get_token
    csrf_token = get_token(request)
    html = f'''
    <!DOCTYPE html>
    <html>
    <head><title>Test Upload</title></head>
    <body style="padding: 20px; font-family: Arial;">
        <h1>Test Cloudinary Upload</h1>
        <form method="POST" enctype="multipart/form-data">
            <input type="hidden" name="csrfmiddlewaretoken" value="{csrf_token}">
            <p><input type="file" name="test_image" accept="image/*" required></p>
            <button type="submit" style="padding: 10px 20px; background: #9b7ec8; color: white; border: none; cursor: pointer;">Test Upload</button>
        </form>
    </body>
    </html>
    '''
    return HttpResponse(html)

def debug_storage(request):
    from django.conf import settings
    return JsonResponse({
        'USE_SUPABASE': getattr(settings, 'USE_SUPABASE', 'NOT SET'),
        'DEFAULT_FILE_STORAGE': getattr(settings, 'DEFAULT_FILE_STORAGE', 'NOT SET'),
        'SUPABASE_URL': getattr(settings, 'SUPABASE_URL', 'NOT SET'),
        'SUPABASE_BUCKET': getattr(settings, 'SUPABASE_BUCKET', 'NOT SET'),
    })



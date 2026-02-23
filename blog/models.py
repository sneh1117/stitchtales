from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify
from django.urls import reverse
import math


class Category(models.Model):
    name=models.CharField(max_length=100)
    slug=models.SlugField(unique=True)
    description=models.TextField(blank=True)
    created_at=models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name_plural="Categories"

    def __str__(self):
        return self.name
    
    def save(self,*args,**kwargs):
        if not self.slug:
            self.slug=slugify(self.name)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("category_detail", kwargs={"slug": self.slug})

class Tag(models.Model):
    name=models.CharField(max_length=100)
    slug=models.SlugField(unique=True)

    def __str__(self):
        return self.name
    
    def save(self,*args,**kwargs):
        if not self.slug:
            self.slug=slugify(self.name)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("tag_detail", kwargs={"slug": self.slug})

# Add this import
def get_supabase_storage():
    from django.conf import settings
    if getattr(settings, 'USE_SUPABASE', False):
        from blog.storage_backends import SupabaseStorage
        return SupabaseStorage()
    return None

class Post(models.Model):
    STATUS_CHOICES=(
        ("draft","Draft"),
        ("published","Published"),
    )

    title=models.CharField(max_length=200)
    slug=models.SlugField(unique=True,blank=True)
    author=models.ForeignKey(User,on_delete=models.CASCADE,related_name="posts")
    category =models.ForeignKey(Category,on_delete=models.SET_NULL,null=True,related_name="posts")
    tags=models.ManyToManyField(Tag,related_name="posts",blank=True)
    cover_image = models.ImageField(
        upload_to="covers/",
        blank=True,
        null=True,
        storage=get_supabase_storage  # ✅ explicitly use Supabase
    )
    content=models.TextField()
    excerpt=models.TextField(max_length=300,blank=True)
    status=models.CharField(max_length=10,choices=STATUS_CHOICES,default="draft")
    view_count=models.PositiveIntegerField(default=0)
    created_at=models.DateTimeField(auto_now_add=True)
    reading_time=models.PositiveIntegerField(default=0)
    updated_at=models.DateTimeField(auto_now=True)


    #SEO fields
    meta_description=models.CharField(
        max_length=160,
        blank=True,
        help_text="SEO meta description (160 chars max)"
    )

    meta_keywords=models.CharField(
        max_length=255,
        blank=True,
        help_text="Comma-separated keywords"
    )


    class Meta:
        ordering=["-created_at"]

    def __str__(self):
        return self.title
    
    def save(self,*args,**kwargs):
        #Auto generate slug from title if not provided
        if not self.slug:
            self.slug=slugify(self.title)
        #Calculate reading time based on content length (assuming 200 words per minute)
        word_count=len(self.content.split())
        self .reading_time=max(1, math.ceil(word_count/200))
        #Auto generate excerpt if not provided
        if not self.excerpt:
            self.excerpt=self.content[:300]
        super().save(*args,**kwargs)
    
    def get_absolute_url(self):
        return reverse("post_detail", kwargs={"slug": self.slug})
    



class UserProfile(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE,related_name="profile")
    bio=models.TextField(max_length=500,blank=True)
    avatar = models.ImageField(
        upload_to="avatars/",
        blank=True,
        null=True,
        storage=get_supabase_storage  # ✅ explicitly use Supabase
    )
    website=models.URLField(blank=True)
    instagram=models.CharField(max_length=100,blank=True)
    pinterest=models.CharField(max_length=100,blank=True)
    created_at=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username}'s Profile"
    


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comments")
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comments")
    content=models.TextField(max_length=1000)
    created_at=models.DateTimeField(auto_now_add=True)
    is_approved=models.BooleanField(default=False)


    class Meta:
        ordering=["created_at"]

    
    def __str__(self):
        return f"Comment by {self.author.username} on {self.post.title}"
    


class Like(models.Model):
    post=models.ForeignKey(Post,on_delete=models.CASCADE,related_name="likes")
    user=models.ForeignKey(User,on_delete=models.CASCADE,related_name="likes")
    created_at=models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together=("post","user")

    def __str__(self):
        return f"{self.user.username} likes {self.post.title}"









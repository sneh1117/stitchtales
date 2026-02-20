from django.contrib import admin
from .models import Post, Category,Tag ,UserProfile,Like,Comment


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display=("title","author","category","status","view_count","reading_time","created_at")
    list_filter=("category","status","created_at")
    search_fields=("title","content","author__username")
    prepopulated_fields={"slug":("title",)}
    list_editable=("status",)
    date_hierarchy="created_at"


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_dispaly=("name","slug")
    prepopulated_fields={"slug":("name",)}


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_dispaly=("name","slug")
    prepopulated_fields={"slug":("name",)}

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display=("user","webiste","created_at")



@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display=("author","post","created_at","is_approved")
    list_filter=("is_approved",)
    list_editable=("is_approved",)

@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
    list_display=("user","post","created_at")


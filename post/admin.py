from django.contrib import admin
from .models import Post, PostFile

class PostFileInline(admin.TabularInline):
    model = PostFile  # Correct: Use the PostFile model directly
    extra = 1

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    inlines = [PostFileInline]
    # ... any other fields for PostAdmin

@admin.register(PostFile)  # Optional: Register PostFile if you want to manage files independently
class PostFileAdmin(admin.ModelAdmin):
    list_display = ['post', 'file']  # Helpful for viewing related posts and files
    search_fields = ['post__caption']  # Allows searching by post caption
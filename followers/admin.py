from django.contrib import admin

# Register your models here.
from .models import Followers

class FollowersAdmin(admin.ModelAdmin):
    pass

admin.site.register(Followers, FollowersAdmin)
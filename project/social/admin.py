from django.contrib import admin

from .models import UserProfile


class UserProfileAdmin(admin.ModelAdmin):
    search_fields = ('user', 'avatar_url')
    ordering = ('user',)
    list_select_related = ('user',)


admin.site.register(UserProfile, UserProfileAdmin)

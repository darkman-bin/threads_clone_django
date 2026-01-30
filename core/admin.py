from django.contrib import admin
from .models import Thread, Profile

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "display_name")
    search_fields = ("user__username", "display_name")


@admin.register(Thread)
class ThreadAdmin(admin.ModelAdmin):
    list_display = ("id", "author", "short_content", "parent", "created_at")
    list_filter = ("created_at",)
    search_fields = ("author__username", "content")

    def short_content(self, obj):
        return (obj.content[:50] + "…") if len(obj.content) > 50 else obj.content

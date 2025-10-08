from django.contrib import admin
from .models import Comment

class CommentAdmin(admin.ModelAdmin):
    list_display = ("id", "recipe", "text", "date_added")
    search_fields = ["text"]
    list_filter = ("date_added",)
    readonly_fields = ("date_added",)

# Register your models here.
admin.site.register(Comment, CommentAdmin)
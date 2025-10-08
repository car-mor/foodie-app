from django.contrib import admin

from recipes.models import Recipe

# Register your models here.
class RecipeAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "category", "date_added")
    search_fields = ["title", "ingredients"]
    list_filter = ("date_added", "category")
    readonly_fields = ("date_added",)





admin.site.register(Recipe, RecipeAdmin)
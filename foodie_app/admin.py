from django.contrib import admin

from .models import Category, Subcategory


class CategoryAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "date_added")
    search_fields = ["name"]
    list_filter = ("date_added",)
    readonly_fields = ("date_added",)


class SubcategoryAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "category", "date_added")
    search_fields = ["name", "category__name"]
    list_filter = ("date_added", "category")
    readonly_fields = ("date_added",)


# Register your models here.
admin.site.register(Category, CategoryAdmin)
admin.site.register(Subcategory, SubcategoryAdmin)

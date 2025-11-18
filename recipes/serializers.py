from django.contrib.auth.models import User
from rest_framework import serializers

from foodie_app.models import Subcategory

from .models import Category, Recipe


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username"]


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["id", "name"]


class SubcategorySerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)

    class Meta:
        model = Subcategory
        fields = ["id", "name", "category"]


class RecipeSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    category = CategorySerializer(read_only=True)
    subcategory = SubcategorySerializer(read_only=True)
    favorited_by = UserSerializer(many=True, read_only=True)

    class Meta:
        model = Recipe
        # fields = "__all__"
        fields = [
            "id",
            "title",
            "description",
            "ingredients",
            "directions",
            "date_added",
            "category",
            "user",
            "image",
            "favorited_by",
        ]
        read_only_fields = ["image"]

from django import forms
from foodie_app.models import Category
from recipes.models import Recipe


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ["name"]
        # labels = {
        #     'name': 'Category Name',
        # }
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter category name', 'autofocus': 'autofocus'}),
        }

class RecipeForm(forms.ModelForm):
    class Meta:
        model = Recipe
        fields = ["title", "description", "ingredients", "directions", "category", "image"]
        # labels = {
        #     'title': 'Recipe Title',
        #     'description': 'Description',
        #     'category': 'Category',
            
        # }
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter recipe title', 'autofocus': 'autofocus'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Enter a brief description'}),
            'ingredients': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'List ingredients'}),
            'directions': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Describe preparation steps'}),
            'category': forms.Select(attrs={'class': 'form-select'}),
            # 'image': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }
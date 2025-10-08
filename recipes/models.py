from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from foodie_app.models import Category

# Create your models here.
class Recipe(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)
    ingredients = models.TextField()
    directions = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE) # many-to-one relationship, if deleted category, delete recipes
    date_added = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name='recipes') # many-to-one relationship, if deleted user, delete recipes
    image = models.ImageField(upload_to='recipe_images/', null=True, blank=True)
    favorited_by = models.ManyToManyField(User, related_name='favorite_recipes', blank=True)

    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse('recipes:recipe_detail', args=[self.id])
from django.db import models
from django.contrib.auth.models import User
from recipes.models import Recipe

# Create your models here.
class Comment(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, related_name='comments')  # Assuming a comment is linked to a recipe
    text = models.TextField()
    date_added = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name='comments')  # Assuming comments are made by users

    def __str__(self):
        return f"Comment by {self.user.username} on {self.recipe.title}"
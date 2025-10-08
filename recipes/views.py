from django.http import HttpResponse, HttpResponseForbidden
from django.shortcuts import get_object_or_404, redirect, render
from django.db.models import Avg, Count, Max, Sum
from django.db.models import Q

from comments.forms import CommentForm
from foodie_app.forms import RecipeForm
from foodie_app.models import Category
from django.contrib.auth.decorators import login_required

from recipes.serializers import RecipeSerializer
from rest_framework import viewsets

from .models import Recipe

# Create your views here.
def recipes(request):
    # recipes = Recipe.objects.get(pk=2)
    # context = {"recipes": recipes}
    # return render(request, "recipes/recipes.html", context)
    # recipes = Recipe.objects.filter(category="Dessert") # Como es foreign key marca error
    # recipes = Recipe.objects.filter(category__name__iexact="Drinks")  # Usando doble guion bajo para acceder al campo name del modelo Category
   
    # recipes = Recipe.objects.exclude(title__contains="revuelto")  # Excluyendo recetas que tengan revuelto en el título
    #category__name__exact="Drinks" # Búsqueda exacta
        #category__name__icontains="drink" # Búsqueda que no distingue mayúsculas de minúsculas
        #category__name__startswith="D" # Búsqueda que empieza por
        #category__name__endswith="s" # Búsqueda que termina por
        #category__name__in=["Drinks", "Dessert"] # Búsqueda en una lista de valores
        #date_added__year=2023, date_added__month=8 # Búsqueda por año y mes
        #category__name__iexact="drinks" # Búsqueda exacta que no distingue mayúsculas de minúsculas, considera espacios
    
    #filter chaining
    # recipes = Recipe.objects.filter(category__name__icontains="dessert").filter(title__icontains="a").order_by("-date_added") # Ordenar por fecha de adición descendente
    
    #slicing querysets
    # recipes = Recipe.objects.all()[:2]  # Obtener las primeras 5 recetas
    
    #aggregation
    # recipes = Recipe.objects.aggregate(Count('id'))  # Contar el número total de recetas
    # recipes = Recipe.objects.aggregate(Avg('id'))  # Promedio de los IDs de las recetas
    # recipes = Recipe.objects.filter(id__gt=2)
    
    #Q objects
    # recipes = Recipe.objects.filter(Q(id__gt=2) | Q(title__startswith="C"))  # Recetas con ID mayor que 2 o título que empieza con 'C'
    # recipes = Recipe.objects.filter(Q(id__gt=2) & Q(title__startswith="C"))  # Recetas con ID mayor que 2 y título que empieza con 'C'
    
    #Values and ValuesList
    # recipes = Recipe.objects.filter(id__gt=2).values()  # Obtener solo los títulos y nombres de categoría de las recetas con ID mayor que 2
    # recipes = Recipe.objects.filter(id__gt=2).values_list()  # Obtener solo los títulos y nombres de categoría de las recetas con ID mayor que 2 
    # recipes = Recipe.objects.filter(id__gt=2).count() 
    # recipes = Recipe.objects.filter(id__gt=2).exists()
    
    #negate
    # recipes = Recipe.objects.filter(~Q(id__gt=2))  # Recetas con ID menor o igual a 2
    recipes = Recipe.objects.all()

    context = {"recipes": recipes}
    # Debugging line to print recipes to the console
    # return HttpResponse("Hello from recipes")
    return render(request, "recipes/recipes.html", context)

def recipe_detail(request, recipe_id):
    # recipe = Recipe.objects.get(pk=recipe_id)
    recipe = get_object_or_404(Recipe, pk=recipe_id)
    comments = recipe.comments.all()  # Obtener todos los comentarios relacionados con la receta
    new_comment = None
    
    if request.method == "POST":
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.recipe = recipe
            new_comment.user = request.user  # Asignar el usuario autenticado al comentario
            new_comment.save()
            return redirect(recipe.get_absolute_url())
    else:
        comment_form = CommentForm()  # ← Mueve esto aquí (fuera del if interno)

    context = {"recipe": recipe, "comments": comments, "comment_form": comment_form}
    return render(request, "recipes/recipe.html", context)

def search_results(request):
    query = request.GET.get("query", "")
    # recipes = Recipe.objects.filter(title__icontains=query) if query else []
    # recipes = Recipe.objects.filter(Q(title__icontains=query) if query else Recipe.objects.none())
    if query:
        
        recipes = Recipe.objects.filter(
            Q(title__icontains=query) | 
            Q(description__icontains=query) |
            Q(ingredients__icontains=query) |
            Q(directions__icontains=query) |
            Q(category__name__icontains=query)
        )
            # ).distinct() if query else [] # Evitar resultados duplicados si una receta coincide en múltiples campos
    #Convertir a set para eliminar duplicados y luego volver a queryset
        seen_ids = set()
        unique_recipes = []
        for recipe in recipes:
            if recipe.id not in seen_ids:
                seen_ids.add(recipe.id)
                unique_recipes.append(recipe)
        recipes = Recipe.objects.filter(id__in=seen_ids)
    else:
        unique_recipes = []  # Retorna un queryset vacío si no hay consulta
    context = {"recipes": unique_recipes, "query": query}
    return render(request, "recipes/search_results.html", context)

@login_required
def toggle_favorite(request, recipe_id):
    recipe = get_object_or_404(Recipe, pk=recipe_id)
    user = request.user

    if user.is_authenticated:
        if user in recipe.favorited_by.all():
            recipe.favorited_by.remove(user)
        else:
            recipe.favorited_by.add(user)
    return redirect("recipes:recipe_detail", recipe_id=recipe.id)

@login_required
def favorite_recipes(request):
    user = request.user
    if user.is_authenticated:
        favorite_recipes = user.favorite_recipes.all()
    else:
        favorite_recipes = Recipe.objects.none()  # Retorna un queryset vacío si el usuario no está autenticado
    context = {"favorite_recipes": favorite_recipes}
    return render(request, "recipes/favorite_recipes.html", context)

@login_required
def delete_recipe(request, recipe_id):
    recipe = get_object_or_404(Recipe, pk=recipe_id)
    #check if the user is the author of the recipe or admin
    if not request.user == recipe.user and not request.user.is_superuser:
        return HttpResponseForbidden("You are not authorized to delete this recipe.")
    
     # Confirm deletion
    if request.method == "POST":
        recipe.delete()
        return redirect("recipes:index")
    context = {"recipe": recipe}
    return render(request, "recipes/recipe_confirmation_delete.html", context)

@login_required
def edit_recipe(request, recipe_id):
    recipe = get_object_or_404(Recipe, pk=recipe_id)
    # Check if the user is the author of the recipe or admin
    if not request.user == recipe.user and not request.user.is_superuser:
        return HttpResponseForbidden("You are not authorized to edit this recipe.")
    
    if request.method == "POST":
        form = RecipeForm(request.POST, request.FILES, instance=recipe)
        if form.is_valid():
            form.save()
            return redirect("recipes:recipe_detail", recipe_id=recipe.id)
    else:
        form = RecipeForm(instance=recipe)
    
    context = {"form": form, "recipe": recipe}
    return render(request, "recipes/recipe_form.html", context)

#Handle http requests
class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
        
        
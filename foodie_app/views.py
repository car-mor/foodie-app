from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required

from foodie_app.forms import CategoryForm, RecipeForm
from .models import Category
from recipes.models import Recipe
# Create your views here.
def index(request):
    categories = Category.objects.all()
    context = {"categories": categories}
    return render(request, "foodie_app/index.html", context)

def recipes(request, category_id):
    category = Category.objects.get(pk=category_id)
    recipes = Recipe.objects.filter(category=category)
    context = {"category": category, "recipes": recipes}
    return render(request, "foodie_app/recipes.html", context)

#If settings.py has LOGIN_URL = 'login', then @login_required will redirect to /login/ like below
# @login_required(login_url='/accounts/login/')

@login_required
def add_category(request):
    if request.method == "POST":
        print(request.POST)
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("foodie_app:index")
        else:
            print(form.errors)
            return render(request, "foodie_app/add_category.html", context)
    else:
    # print(request)
        form = CategoryForm()
        context = {"form": form}
    return render(request, "foodie_app/add_category.html", context)

# def add_recipe(request):
#     if request.method == "POST":
#         print(request.POST)
#         form = RecipeForm(request.POST)
#         if form.is_valid():
#             form.save()
#             return redirect("recipes:index")
#         else:
#             form = RecipeForm()
#             context = {"form": form}
#             return render(request, "foodie_app/add_recipe.html", context)
#     else:
#         form = RecipeForm()
#         context = {"form": form}
#     return render(request, "foodie_app/add_recipe.html", context)

@login_required
def add_recipe(request, category_id=None):
    category = None
    initial_data = {}
    
    if category_id:
        category = get_object_or_404(Category, pk=category_id)
        initial_data = {"category": category}
    
    if request.method == "POST":
        form = RecipeForm(request.POST, request.FILES)  # ← Sin initial aquí
        if form.is_valid():
            new_recipe = form.save(commit=False)
            new_recipe.user = request.user
            new_recipe.save()
            return redirect("foodie_app:recipes", category_id=new_recipe.category.id)
    else:
        form = RecipeForm(initial=initial_data)  # ← initial solo para GET
    
    context = {"form": form, "category": category}
    return render(request, "recipes/add_recipe.html", context)
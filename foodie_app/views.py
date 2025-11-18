from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render

from foodie_app.forms import RecipeForm
from recipes.models import Recipe

from .models import Category, Subcategory


# Create your views here.
def index(request):
    categories = Category.objects.all()
    context = {"categories": categories}
    return render(request, "foodie_app/index.html", context)


def category_detail(request, category_id):
    category = get_object_or_404(Category, pk=category_id)
    # Cargar todas las subcategorías asociadas a esta categoría
    subcategories = category.subcategories.all()

    # Renderizará una plantilla que lista las subcategorías
    context = {"category": category, "subcategories": subcategories}
    return render(request, "foodie_app/subcategories_list.html", context)


def subcategory_recipes(request, subcategory_id):
    subcategory = get_object_or_404(Subcategory, pk=subcategory_id)
    # Filtrar las recetas por la subcategoría
    # NOTA: Necesitas una relación ForeignKey o ManyToManyField en el modelo Recipe
    # Asumiré que el campo en Recipe se llama 'subcategory' por ahora:
    recipes = Recipe.objects.filter(subcategory=subcategory)

    # Renderizará una plantilla que lista las recetas
    context = {"subcategory": subcategory, "recipes": recipes}
    return render(request, "foodie_app/recipes_list.html", context)


# If settings.py has LOGIN_URL = 'login', then @login_required will redirect to /login/ like below
# @login_required(login_url='/accounts/login/')

# @login_required
# def add_category(request):
#     if request.method == "POST":
#         print(request.POST)
#         form = CategoryForm(request.POST)
#         if form.is_valid():
#             form.save()
#             return redirect("foodie_app:index")
#         else:
#             print(form.errors)
#             return render(request, "foodie_app/add_category.html", context)
#     else:
#     # print(request)
#         form = CategoryForm()
#         context = {"form": form}
#     return render(request, "foodie_app/add_category.html", context)

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


# foodie_app/views.py (función add_recipe refactorizada)


# foodie_app/views.py (función add_recipe)


@login_required
def add_recipe(request, subcategory_id=None):
    subcategory = None
    category = None
    lock_fields = (
        False  # Flag para indicarle al formulario si debe bloquear/ocultar los campos
    )
    form_kwargs = {}  # Argumentos para instanciar RecipeForm

    if subcategory_id:
        # Estamos en el flujo 'add_recipe_to_subcategory'
        subcategory = get_object_or_404(Subcategory, pk=subcategory_id)
        category = subcategory.category
        lock_fields = True  # ¡Bloqueamos/Ocultamos los campos!

        # Pasamos las instancias y el flag al formulario
        form_kwargs = {
            "category": category,
            "subcategory": subcategory,
            "lock_fields": lock_fields,
        }

    if request.method == "POST":
        # 1. Instanciamos el formulario, pasando los datos POST y los kwargs
        form = RecipeForm(request.POST, request.FILES, **form_kwargs)

        if form.is_valid():
            new_recipe = form.save(commit=False)
            new_recipe.user = request.user

            # 2. ASIGNACIÓN CONDICIONAL (Sólo si los campos estaban bloqueados)
            if lock_fields:
                # Asignación forzada para el flujo 'to_subcategory'
                new_recipe.subcategory = subcategory
                new_recipe.category = category
            # Si NO está bloqueado (lock_fields=False), los datos vienen del POST del usuario

            new_recipe.save()

            # 3. Redirección
            if new_recipe.subcategory:
                return redirect(
                    "foodie_app:subcategory_recipes",
                    subcategory_id=new_recipe.subcategory.id,
                )
            else:
                return redirect(new_recipe)
        else:
            # Si el formulario es inválido, renderizamos con el formulario y los errores
            context = {
                "form": form,
                "subcategory": subcategory,
                "category": category,
                "lock_fields": lock_fields,
            }
            return render(request, "recipes/add_recipe.html", context)
    else:
        # Para peticiones GET
        form = RecipeForm(**form_kwargs)

    context = {
        "form": form,
        "subcategory": subcategory,
        "category": category,
        "lock_fields": lock_fields,
    }
    return render(request, "recipes/add_recipe.html", context)


def load_subcategories(request):
    """
    Vista AJAX para cargar subcategorías basadas en la categoría seleccionada.
    """
    # 1. Obtener el ID de la Categoría de la solicitud GET
    category_id = request.GET.get("category_id")

    # 2. Filtrar Subcategorías
    if category_id:
        subcategories = Subcategory.objects.filter(category_id=category_id).order_by(
            "name"
        )
    else:
        # Si no se proporciona ID, devolvemos un QuerySet vacío
        subcategories = Subcategory.objects.none()

    # 3. Formatear la respuesta como una lista de diccionarios (valor, texto)
    # [{"id": 1, "name": "Mexicana"}, ...]
    data = [
        {"id": subcategory.id, "name": subcategory.name}
        for subcategory in subcategories
    ]

    return JsonResponse(data, safe=False)

from django.urls import path

from . import views

app_name = "foodie_app"
urlpatterns = [
    path("", views.index, name="index"),
    # PRIMER NIVEL: Clic en Categoría -> Lista Subcategorías
    path("category/<int:category_id>/", views.category_detail, name="category_detail"),
    # SEGUNDO NIVEL: Clic en Subcategoría -> Lista Recetas
    path(
        "subcategory/<int:subcategory_id>/",
        views.subcategory_recipes,
        name="subcategory_recipes",
    ),
    # Recetas específicas
    # Aquí puedes mantener las URLs existentes de 'add-recipe'
    path("add-recipe/", views.add_recipe, name="add_recipe_no_context"),
    path(
        "add-recipe/<int:subcategory_id>/",
        views.add_recipe,
        name="add_recipe_to_subcategory",
    ),
    path(
        "ajax/load-subcategories/",
        views.load_subcategories,
        name="ajax_load_subcategories",
    ),
]

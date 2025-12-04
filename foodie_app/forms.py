from django import forms

from foodie_app.models import Category, Subcategory
from recipes.models import Recipe


class SubcategoryModelChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        return obj.name


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ["name"]
        widgets = {
            "name": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Enter category name",
                    "autofocus": "autofocus",
                }
            ),
        }


# foodie_app/forms.py
# foodie_app/forms.py


class RecipeForm(forms.ModelForm):
    # 1. AGREGAR 'label' AQUÍ para campos definidos manualmente
    category = forms.ModelChoiceField(
        label="Categoría",  # <--- Nombre en español
        queryset=Category.objects.all(),
        required=True,
        widget=forms.Select(
            attrs={
                "class": "form-select",
                "id": "id_category",
            }
        ),
    )

    subcategory = SubcategoryModelChoiceField(
        label="Subcategoría",  # <--- Nombre en español
        queryset=Subcategory.objects.all(),
        required=False,
        widget=forms.Select(
            attrs={
                "class": "form-select",
                "id": "id_subcategory",
                "disabled": "disabled",
            }
        ),
    )

    def __init__(self, *args, **kwargs):
        # ... (Tu código __init__ existente se mantiene igual) ...
        self.category_instance = kwargs.pop("category", None)
        self.subcategory_instance = kwargs.pop("subcategory", None)
        lock_fields = kwargs.pop("lock_fields", False)

        super().__init__(*args, **kwargs)

        if lock_fields:
            del self.fields["category"]
            del self.fields["subcategory"]

        if (
            not kwargs.get("lock_fields", False)
            and self.is_bound
            and not self.errors.get("category")
        ):
            self.fields["subcategory"].widget.attrs.pop("disabled", None)
        else:
            pass

    class Meta:
        model = Recipe
        fields = [
            "title",
            "description",
            "ingredients",
            "directions",
            "category",
            "subcategory",
            "image",
        ]

        # 2. AGREGAR EL DICCIONARIO 'labels' AQUÍ
        labels = {
            "title": "Título de la receta",
            "description": "Descripción breve",
            "ingredients": "Ingredientes",
            "directions": "Instrucciones / Pasos",
            "image": "Imagen (opcional)",
        }

        # 3. ACTUALIZAR LOS TEXTOS DE LOS WIDGETS A ESPAÑOL
        widgets = {
            "title": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Introduce el título de la receta",  # <--- Español
                    "autofocus": "autofocus",
                }
            ),
            "description": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "placeholder": "Escribe una descripción breve",  # <--- Español
                    "rows": 3,  # Opcional: hace la caja un poco más pequeña visualmente
                }
            ),
            "ingredients": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "placeholder": "Lista los ingredientes uno por uno...",  # <--- Español
                }
            ),
            "directions": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "placeholder": "Describe los pasos de preparación...",  # <--- Español
                }
            ),
        }

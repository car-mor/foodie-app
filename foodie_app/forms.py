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


class RecipeForm(forms.ModelForm):
    # Usamos el campo personalizado, pero lo definimos aquí para el widget

    # 🚨 CORRECCIÓN AQUÍ: Definir widget y attrs, incluyendo el ID
    category = forms.ModelChoiceField(
        queryset=Category.objects.all(),
        required=True,
        widget=forms.Select(
            attrs={
                "class": "form-select",
                "id": "id_category",  # <-- CRÍTICO para el JavaScript
            }
        ),
    )

    # 🚨 CORRECCIÓN AQUÍ: Definir widget, attrs y el estado inicial 'disabled'
    subcategory = SubcategoryModelChoiceField(
        queryset=Subcategory.objects.all(),
        required=False,
        widget=forms.Select(
            attrs={
                "class": "form-select",
                "id": "id_subcategory",  # <-- CRÍTICO para el JavaScript
                "disabled": "disabled",  # <-- Estado inicial para el flujo 'no_context'
            }
        ),
    )

    def __init__(self, *args, **kwargs):
        # Extraer las instancias y el flag 'lock_fields'
        self.category_instance = kwargs.pop("category", None)
        self.subcategory_instance = kwargs.pop("subcategory", None)
        lock_fields = kwargs.pop("lock_fields", False)

        super().__init__(*args, **kwargs)

        # 2. Lógica de Bloqueo/Ocultación
        if lock_fields:
            # Flujo 'add_recipe_to_subcategory': Se asigna forzadamente en la vista.

            # 🚨 Si quieres OCULTAR los campos del usuario:
            del self.fields["category"]
            del self.fields["subcategory"]

            # Si quieres MOSTRARLOS pero deshabilitados (solo lectura), usarías:
            # self.fields['category'].disabled = True
            # self.fields['subcategory'].disabled = True

            # Además, dado que la vista (views.py) está a cargo de asignarlos,
            # no necesitamos que el formulario los valide, por lo que marcarlos
            # como opcionales (False) es bueno si se mantienen visibles.

            # Asignar valores iniciales para asegurar que se utilicen en caso de que
            # el formulario se mantenga visible y solo desactivado:
            # if self.category_instance:
            #     self.initial['category'] = self.category_instance
            # if self.subcategory_instance:
            #     self.initial['subcategory'] = self.subcategory_instance

        if (
            not kwargs.get("lock_fields", False)
            and self.is_bound
            and not self.errors.get("category")
        ):
            # Si hay datos y la categoría no tiene errores, habilitamos la subcategoría
            # (el JS se encargará de rellenar las opciones)
            self.fields["subcategory"].widget.attrs.pop("disabled", None)

        else:
            # Flujo 'add_recipe_no_context': El usuario debe seleccionarlos
            # Aquí podríamos agregar un filtro inicial para las subcategorías (ver punto 3)
            pass

    class Meta:
        model = Recipe
        # Incluímos category y subcategory aquí para que estén disponibles por defecto
        fields = [
            "title",
            "description",
            "ingredients",
            "directions",
            "category",
            "subcategory",
            "image",
        ]
        # ... widgets...
        widgets = {
            "title": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Enter recipe title",
                    "autofocus": "autofocus",
                }
            ),
            "description": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "placeholder": "Enter a brief description",
                }
            ),
            "ingredients": forms.Textarea(
                attrs={"class": "form-control", "placeholder": "List ingredients"}
            ),
            "directions": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "placeholder": "Describe preparation steps",
                }
            ),
            # Category y Subcategory usan los widgets de los campos ModelChoiceField definidos arriba
        }

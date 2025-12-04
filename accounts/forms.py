from django import forms

from .models import UserProfile


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ["bio", "profile_photo"]

        # 1. Etiquetas en Español
        labels = {
            "bio": "Biografía / Sobre mí",
            "profile_photo": "Foto de Perfil",
        }

        # 2. Estilos (Bootstrap) y Placeholders
        widgets = {
            "bio": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 4,
                    "placeholder": "Cuéntanos qué te gusta cocinar, tus platillos favoritos...",
                }
            ),
            # ClearableFileInput permite limpiar la imagen si ya existe una
            "profile_photo": forms.ClearableFileInput(attrs={"class": "form-control"}),
        }

        # 3. Mensajes de ayuda opcionales (se muestran bajo el campo)
        help_texts = {
            "profile_photo": "Sube una imagen (preferiblemente cuadrada) para tu avatar.",
        }

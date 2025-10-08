from django.urls import path, include
from .views import edit_user_profile, register

app_name = "accounts"

urlpatterns = [
    path("register/", register, name="register"),
    # path('accounts/', include('django.contrib.auth.urls')),
    path('', include('django.contrib.auth.urls')),
    path('edit_profile/', edit_user_profile, name='edit_user_profile'),
]
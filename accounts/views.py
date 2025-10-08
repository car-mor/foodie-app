from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login

from accounts.forms import UserProfileForm

# Create your views here.
def register(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)  # ← aquí van los datos del POST
        if form.is_valid():
            new_user = form.save()
            # Log the user in
            login(request, new_user)
            return redirect("foodie_app:index")
            # O mejor: return redirect("home") para redirigir a otra página
    else:
        form = UserCreationForm()  # ← en GET se muestra el formulario vacío

    context = {"form": form}
    return render(request, "registration/register.html", context)

def edit_user_profile(request):
    if request.method == "POST":
        form = UserProfileForm(request.POST, request.FILES, instance=request.user.profile)
        if form.is_valid():
            form.save()
            return redirect("foodie_app:index")
    else:
        form = UserProfileForm(instance=request.user.profile)

    context = {"form": form}
    return render(request, "registration/edit_profile.html", context)
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.views.generic import ListView, DetailView, View

from recipes.models import Recipe
from sandbox.forms import FeedbackForm
from sandbox.models import Feedback
from django.contrib import messages
# from random import choice

# fruits = ["apple", "banana", "cherry"]

# Create your views here.
def index(request):
    # data = "Sample Data"
    # data = {"key": "value", "number": 42}
    # data = {"key": choice(fruits)}
    # data = choice(fruits)
    # return HttpResponse(f"Hello, world. You're at the sandbox index. Here's the data: {data['key']}")
    # return HttpResponse(f"Hello there, {data['key']}")
    # return HttpResponse(f"Hello there, {data}")
    # data = {
    #     "name": "Carlos",
    #     "age": 30,
    #     "city": "New York",
    #     "hobbies": ["reading", "traveling", "coding"],
    # }
    recipes = Recipe.objects.all()
    context = {"recipes": recipes}
    return render(request, "sandbox/index.html", context)

class RecipeListView(ListView):
    model = Recipe
    template_name = "sandbox/index.html"
    # object_list
    
    context_object_name = "recipes"
    
    def get_queryset(self):
        filtered_recipes = Recipe.objects.filter(category__name__iexact="drinks")
        return filtered_recipes
    
    
class RecipeDetailView(DetailView):
    model = Recipe
    template_name = "sandbox/recipe_detail.html"
    context_object_name = "recipe"

# Custom class based views
class SpecificRecipesView(View):
    def get(self, request, *args, **kwargs):
        #fetch recipes with "refreshing" in description
        refreshing_recipes = Recipe.objects.filter(description__icontains="refreshing")
        context = {"refreshing": refreshing_recipes}
        
        return render(request, "sandbox/refreshing_recipes.html", context)

def thank_you(request):
    return HttpResponse("Thank you for your feedback!")

def feedback(request):
    request.session['feedback_visits'] = request.session.get('feedback_visits', 0) + 1
    #to delete sessions
    # if "feedback_visits" in request.session:
    #     del request.session['feedback_visits']
    # request.session.clear() another option
    
    # request.session.flush() #saves session data
    
    # print("Expires in:", request.session.get_expiry_age()//86400, "days" )
    if request.method == "POST":
        form = FeedbackForm(request.POST)
        if form.is_valid():
            #save form data to session
            request.session['feedback_data'] = form.cleaned_data
            return redirect("sandbox:feedback_review")
        
            # print(form.cleaned_data)
            # Feedback.objects.create(
            #     name=form.cleaned_data['name'],
            #     email=form.cleaned_data['email'],
            #     feedback=form.cleaned_data['feedback'],
            #     satisfaction=form.cleaned_data['satisfaction']
            # )
            # messages.add_message(request, messages.SUCCESS, "Thank you for your feedback!")
            # messages.success(request, "Thank you for your feedback!")

            # return redirect("sandbox:index")
    else:
        form = FeedbackForm()

    context = {
        "form": form,
        "visits": request.session['feedback_visits']
    }
    return render(request, "sandbox/feedback_form.html", context)


def feedback_review(request):
    # feedback_data = request.session.get('feedback_data', {})
    feedback_data = request.session.get('feedback_data')
    if not feedback_data:
        messages.error(request, "No feedback data found. Please submit the feedback form first.")
        return redirect("sandbox:feedback")
    
    if request.method == "POST":
        #save feedback data to database
        # Feedback.objects.create(
        #     name=feedback_data['name'],
        #     email=feedback_data['email'],
        #     feedback=feedback_data['feedback'],
        #     satisfaction=feedback_data['satisfaction']
        # )
        Feedback.objects.create(**feedback_data)
        #clear feedback data from session
        del request.session['feedback_data']
        messages.success(request, "Thank you for your feedback!")
        return redirect("sandbox:index")
    form = FeedbackForm(initial=feedback_data)
    
    context = {
        "form": form,
    }
    return render(request, "sandbox/feedback_review.html", context)
from django import forms
from .models import Comment

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']
        labels = {'text':''}
        widgets = {
            'text': forms.Textarea(attrs={'class': 'form-control', 'rows': 8, 'cols': 40, 'placeholder': 'Enter your comment here...'}),
        }
        
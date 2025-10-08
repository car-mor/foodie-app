from django import forms

choices = [
    ('very_satisfied', 'Very Satisfied'),
    ('satisfied', 'Satisfied'),
    ('neutral', 'Neutral'),
    ('dissatisfied', 'Dissatisfied'),
    ('very_dissatisfied', 'Very Dissatisfied')
]
class FeedbackForm(forms.Form):
    name = forms.CharField(max_length=100, label='Your Name')
    email = forms.EmailField(label='Your Email')
    feedback = forms.CharField(label='Your Feedback')
    satisfaction = forms.ChoiceField(
        choices=choices,
        widget=forms.RadioSelect,
        label='Satisfaction Level'
    )
    
    def clean_email(self):
        # email = self.cleaned_data.get('email')
        email = self.cleaned_data['email']
        if "@gmail.com" not in email and "@yahoo.com" not in email:
            raise forms.ValidationError("Email must be from the domain '@gmail.com' or '@yahoo.com'.")
        return email
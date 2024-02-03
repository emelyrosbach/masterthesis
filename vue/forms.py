from django import forms

class Registration(forms.Form):
    email = forms.EmailField(label="Your email", required=True)

class PreStudy(forms.Form):
    gender = forms.CharField(label="Your gender?", required=True)

class PostStudy(forms.Form):
    UEQS = forms.CharField(label="UEQS", required=True)

class Confidence(forms.Form):
    CHOICES = [
        ('1', 'not confident at all'),
        ('2', ''),
        ('3', ''),
        ('4', ''),
        ('5', 'completely confident'),
    ]
    likertScale = forms.ChoiceField(
        widget=forms.RadioSelect,
        choices=CHOICES,
        label="likertScale",
        required=True
    )

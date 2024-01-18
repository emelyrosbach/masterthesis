from django import forms

class Registration(forms.Form):
    email = forms.EmailField(label="Your email", required=True)

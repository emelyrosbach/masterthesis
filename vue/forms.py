from django import forms

class Registration(forms.Form):
    email = forms.EmailField(label="Your email", required=True)

class PreStudy(forms.Form):
    gender = forms.CharField(label="Your gender?", required=True)

class PostStudy(forms.Form):
    UEQS = forms.CharField(label="UEQS", required=True)

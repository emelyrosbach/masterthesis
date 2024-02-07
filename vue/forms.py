from django import forms

class Registration(forms.Form):
    email = forms.EmailField(label="", required=True, widget=forms.TextInput(
    attrs={'type': 'email',
           'placeholder': ('example@app.com')}))
    terms = forms.BooleanField(required=True) 

class PreStudy(forms.Form):
    GENDEROPTS = [
        ('Male', 'Male'),
        ('Female', 'Female'),
        ('Prefer not to say', 'Prefer not to say'),
        ('Other', 'Other'),
    ]
    gender = forms.ChoiceField(
        widget=forms.RadioSelect,
        choices=GENDEROPTS,
        label="What gender do you identify as?",
        required=True
    )
    AGEOPTS = [
        ('<18', '<18'),
        ('18-24', '18-24'),
        ('25-34', '25-34'),
        ('35-44', '35-44'),
        ('45-54', '45-54'),
        ('>55', '>55'),
    ]
    age = forms.ChoiceField(
        widget=forms.RadioSelect,
        choices=AGEOPTS,
        label="What is your Age?",
        required=True
    )
    EXPOPTS = [
        ('<5 years', '<5 years'),
        ('5-10 years', '5-10 years'),
        ('10-15 years', '10-15 years'),
        ('>15 years', '>15years'),
    ]
    experience = forms.ChoiceField(
        widget=forms.RadioSelect,
        choices=EXPOPTS,
        label="What is the duration of your experience working in the mediacal field?",
        required=True
    )
    INTERESTOPTS = [
        ('5', 'Very interested in technology'),
        ('4', 'Somehow interested in technology'),
        ('3', 'Indifferent about technology'),
        ('2', 'Less interested in technology'),
        ('1', 'Not at all interested in technology'),
    ]
    interest = forms.ChoiceField(
        widget=forms.RadioSelect,
        choices=INTERESTOPTS,
        label="How interested in technology would you describe yourself?",
        required=True
    )
    ADOPTOPTS = [
        ('4', 'I will try out the app as soon as possible.'),
        ('3', 'I will start using the app as soon as it becomes popular among my acquaintances.'),
        ('2', 'I will eventually give in to using the app, despite initially resisting it.'),
        ('1', 'I will strongly oppose the use of the app'),
    ]
    adopt = forms.ChoiceField(
        widget=forms.RadioSelect,
        choices=ADOPTOPTS,
        label="A new messenger app is coming onto the market. Which statement applies to you?",
        required=True
    )
    AIEXPOPTS = [
        ('4', 'Very much familiar'),
        ('3', 'Somewhat familiar'),
        ('2', 'Less familiar'),
        ('1', 'Not at all familiar'),
    ]
    aiexp = forms.ChoiceField(
        widget=forms.RadioSelect,
        choices=AIEXPOPTS,
        label="How familiar are you with artificial intelligence?",
        required=True
    )

class PostStudy(forms.Form):
    CHOICES = [
        ('1', ''),
        ('2', ''),
        ('3', ''),
        ('4', ''),
        ('5', ''),
        ('6', ''),
        ('7', ''),
    ]
    item1 = forms.ChoiceField(
        widget=forms.RadioSelect,
        choices=CHOICES,
        label="",
        required=True
    )
    item2 = forms.ChoiceField(
        widget=forms.RadioSelect,
        choices=CHOICES,
        label="",
        required=True
    )
    item3 = forms.ChoiceField(
        widget=forms.RadioSelect,
        choices=CHOICES,
        label="",
        required=True
    )
    item4 = forms.ChoiceField(
        widget=forms.RadioSelect,
        choices=CHOICES,
        label="",
        required=True
    )
    item5 = forms.ChoiceField(
        widget=forms.RadioSelect,
        choices=CHOICES,
        label="",
        required=True
    )
    item6 = forms.ChoiceField(
        widget=forms.RadioSelect,
        choices=CHOICES,
        label="",
        required=True
    )
    item7 = forms.ChoiceField(
        widget=forms.RadioSelect,
        choices=CHOICES,
        label="",
        required=True
    )
    item8 = forms.ChoiceField(
        widget=forms.RadioSelect,
        choices=CHOICES,
        label="",
        required=True
    )

class Confidence(forms.Form):
    CHOICES = [
        ('1', ''),
        ('2', ''),
        ('3', ''),
        ('4', ''),
        ('5', ''),
    ]
    likertScale = forms.ChoiceField(
        widget=forms.RadioSelect,
        choices=CHOICES,
        label="",
        required=True
    )

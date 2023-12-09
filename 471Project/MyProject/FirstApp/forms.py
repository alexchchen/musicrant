from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class RegisterForm(UserCreationForm):
    fname = forms.CharField(label='First name', max_length=15)
    lname = forms.CharField(label='Last name', max_length=15)
    age = forms.IntegerField(label='Age')
    gender = forms.CharField(label='Gender', max_length=15)

    class Meta:
        model = User
        fields = ["username", "password1", "password2", "fname", "lname", "age", "gender"]
        
    def clean(self):
        super(RegisterForm, self).clean()
        
        age = self.cleaned_data.get('age')
        
        if age < 1:
            self.add_error('age', 'Minimum age is 1.')
        if age > 120:
            self.add_error('age', 'Maximum age is 120.')
from django import forms
from django.forms import Form
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

SCORE_CHOICES = [
    (0, '0'),
    (1, '1'),
    (2, '2'),
    (3, '3'),
    (4, '4'),
    (5, '5'),
    (6, '6'),
    (7, '7'),
    (8, '8'),
    (9, '9'),
    (10, '10')
]


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
            

class SongRatingForm(Form):
    originality_score = forms.ChoiceField(label='Originality Score', choices=SCORE_CHOICES)
    lyric_score = forms.ChoiceField(label='Lyric Score', choices=SCORE_CHOICES)
    vibe_score = forms.ChoiceField(label='Vibe Score', choices=SCORE_CHOICES)
    instrumental_score = forms.ChoiceField(label='Instrumental Score', choices=SCORE_CHOICES)
    
class AlbumRatingForm(Form):
    originality_score = forms.ChoiceField(label='Originality Score', choices=SCORE_CHOICES)
    lyric_score = forms.ChoiceField(label='Lyric Score', choices=SCORE_CHOICES)
    vibe_score = forms.ChoiceField(label='Vibe Score', choices=SCORE_CHOICES)
    instrumental_score = forms.ChoiceField(label='Instrumental Score', choices=SCORE_CHOICES)
    album_flow_score = forms.ChoiceField(label='Album Flow Score', choices=SCORE_CHOICES)
    
class SongReviewForm(Form):
    title = forms.CharField(label="Title")
    body = forms.CharField(label="Body", widget=forms.Textarea)
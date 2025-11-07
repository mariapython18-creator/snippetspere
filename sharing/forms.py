from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser, Snippet, DeveloperProfile,Question,Answer


class Register(UserCreationForm):
    email = forms.EmailField(required=True)
    class Meta:
        model=CustomUser
        fields=['username', 'email', 'password1', 'password2',
            'phone_number','role']

class Snippet_form(forms.ModelForm):
    class Meta:
        model = Snippet
        exclude = ['user']  # 👈 exclude user from form

class Developer_form(forms.ModelForm):
    class Meta():
        model=DeveloperProfile
        fields='__all__'
class Login_form(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)
class Question_form(forms.ModelForm):
    class Meta():
        model=Question
        fields=[ 'Language', 'Description', 'code_snippet', 'Question']
from django import forms
from .models import Answer

class Answerform(forms.ModelForm):
    class Meta:
        model = Answer
        fields = ['Answer', 'code_snippet']  # exactly your model fields
        widgets = {
            'Answer': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Write your answer here...'
            }),
            'code_snippet': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Optional: Add code snippet...'
            }),
        }
# from django import forms
# from .models import CollaborationRequest
#



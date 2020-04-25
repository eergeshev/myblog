from django import forms
from django.contrib.auth.models import User
from .models import Comment, Blogger, Blog
from django.contrib.auth.forms import UserChangeForm, UserCreationForm


class CommentForm(forms.ModelForm):
    
    class Meta:
            model = Comment
            
            fields = ['body',]

class EditBloggerForm(forms.ModelForm):
    class Meta:
        model = Blogger
        fields = (
            'bio',
        )

class EditUserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('username','first_name', 'last_name', 'email')

class SelfBlogForm(forms.ModelForm):
    class Meta:
        model = Blog
        fields = ('title', 'description')

class SignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=100, help_text='Last Name')
    last_name = forms.CharField(max_length=100, help_text='Last Name')
    email = forms.EmailField(max_length=150, help_text='Email')
    
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2',)
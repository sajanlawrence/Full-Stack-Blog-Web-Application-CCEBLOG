from django import forms
from blog.models import Post, Comment, UserProfileInfo
from django.contrib.auth.models import User

class UserForm(forms.ModelForm): 
    class Meta:
        model = User
        fields = ('username','email','password','first_name','last_name')
        widgets = {
            'username' : forms.TextInput(attrs={'class':'form-control','placeholder':'Enter your username'}),
            'email' : forms.TextInput(attrs={'class':'form-control','placeholder':'Enter your email'}),
            'password' : forms.PasswordInput(attrs={'class':'form-control','placeholder':'Enter your password'}),
            'first_name' : forms.TextInput(attrs={'class':'form-control','placeholder':'Enter your first name'}),
            'last_name' : forms.TextInput(attrs={'class':'form-control','placeholder':'Enter your last name'}),
        }

class UserProfileInfoForm(forms.ModelForm):
    class Meta:
        model = UserProfileInfo
        fields = ('bio','instagram','linkedin','facebook','twitter','picture')
        widgets = {
            'bio' : forms.Textarea(attrs={'rows':'5','class':'form-control','placeholder':'Tell us little about you'}),
            }

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('title','support_content','text')
        #widget is used for edit the fields using css. It is a dictionary where key will be the field name.
        widgets = {
            'title' : forms.TextInput(attrs={'class':'form-control','placeholder':'Enter your post title here'}),
            'support_content' : forms.TextInput(attrs={'class':'form-control','placeholder':'Write a short note about your post'}),
            'text' : forms.Textarea(attrs={'class': 'form-control','placeholder':'Type your post here'}),
        }

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('text',)
        widgets = {
            'text' : forms.Textarea(attrs={'class':'form-control'}),
        }
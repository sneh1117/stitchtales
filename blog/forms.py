from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from models import UserProfile,Post, Comment



class RegistrationForm(UserCreationForm):
    email=forms.EmailField(required=True)
    first_name=forms.CharField(max_length=30, required=True)
    last_name=forms.CharField(max_length=30, required=True)


    class Meta:
        model=User
        fields=["username","email","first_name","last_name","password1","password2"]


class UserUpdateForm(forms.ModelForm):
    email=forms.EmailField(required=True)


    class Meta:
        model=User
        fields=["username","first_name","last_name","email"]


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model=UserProfile
        fields=["bio","avatar","website","instagram","pinterest"]
        widgets={
            "bio":forms.Textarea(attrs={"rows":4}), }
        

class PostForm(forms.ModelForm):
    class Meta:
        model=Post
        fields=["title","category","tags","cover_image","content","excerpt","status"]
        widgets={
            "content":forms.Textarea(attrs={"rows":15}),
            "excerpt":forms.Textarea(attrs={"rows":3}),}
        

class CommentForm(forms.ModelForm):
    class Meta:
        model=Comment
        fields=["content"]
        widgets={
            "content":forms.Textarea(attrs={"rows":3, "placeholder":"Share your thoughts here ..."}),}
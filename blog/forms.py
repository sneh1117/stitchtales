from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import UserProfile,Post, Comment,Tag



class RegisterForm(UserCreationForm):
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
    tags = forms.ModelMultipleChoiceField(
        queryset=Tag.objects.all(),
        widget=forms.CheckboxSelectMultiple(),
        required=False
    )

    class Meta:
        model = Post
        fields = ['title', 'category', 'tags', 'cover_image', 'content', 'excerpt', 'status']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'category': forms.Select(attrs={'class': 'form-control'}),
            'cover_image': forms.FileInput(attrs={'class': 'form-control'}),
            'content': forms.Textarea(attrs={'rows': 15, 'class': 'form-control'}),
            'excerpt': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
        }
        

class CommentForm(forms.ModelForm):
    class Meta:
        model=Comment
        fields=["content"]
        widgets={
            "content":forms.Textarea(attrs={"rows":3, "placeholder":"Share your thoughts here ..."}),}
        


#add Bootstrap styling to all form fileds automatically 
for form_class in [RegisterForm,UserUpdateForm,ProfileUpdateForm,PostForm,CommentForm]:
    for field in form_class.base_fields.values():
        if hasattr(field,"widget"):
            field.widget.attrs.update({'class':'form-control'})
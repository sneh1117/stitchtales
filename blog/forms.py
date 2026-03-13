from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import UserProfile, Post, Comment, Tag, PostImage


class MultipleFileInput(forms.ClearableFileInput):
    """Custom widget to allow multiple file uploads"""
    allow_multiple_selected = True


class MultipleFileField(forms.FileField):
    """Custom field to handle multiple file uploads"""
    def __init__(self, *args, **kwargs):
        kwargs.setdefault("widget", MultipleFileInput())
        super().__init__(*args, **kwargs)

    def clean(self, data, initial=None):
        single_file_clean = super().clean
        if isinstance(data, (list, tuple)):
            result = [single_file_clean(d, initial) for d in data]
        else:
            result = single_file_clean(data, initial)
        return result


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
    
    # ALLOW UP TO 3 COVER IMAGES WITH VALIDATION
    cover_images = MultipleFileField(
        required=False,
        label='Cover Images (Max 3)',
        help_text='Upload 1-3 images. Click to enlarge in post.'
    )

    class Meta:
        model = Post
        fields = ['title', 'category', 'tags', 'content', 'excerpt', 'status']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'category': forms.Select(attrs={'class': 'form-control'}),
            'content': forms.Textarea(attrs={'rows': 15, 'class': 'form-control'}),
            'excerpt': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
        }
    
    def clean_cover_images(self):
        """Validate that max 3 images are uploaded"""
        cover_images = self.files.getlist('cover_images')
        
        if len(cover_images) > 3:
            raise forms.ValidationError('You can upload a maximum of 3 images. You selected ' + str(len(cover_images)) + '.')
        
        return cover_images
    
    def save(self, commit=True):
        post = super().save(commit=commit)
        
        if commit:
            # Delete existing images for this post
            post.images.all().delete()
            
            # Save new cover images (max 3)
            cover_images = self.files.getlist('cover_images')
            
            for order, image in enumerate(cover_images[:3]):  # Limit to 3 (extra safety)
                if image:  # Only save if image exists
                    PostImage.objects.create(
                        post=post,
                        image=image,
                        order=order
                    )
        
        return post

        

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
            if not isinstance(field.widget, MultipleFileInput):  # Don't override custom widget
                field.widget.attrs.update({'class':'form-control'})
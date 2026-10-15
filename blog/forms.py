from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import Post


class registrationform(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = (
            'username',
            'email',
            'password1',
            'password2',
        )


class PostForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = [
            'title',
            'slug',
            'content',
            'cover_image',
            'status',
            'category',
            'tags',
        ]

        widgets = {
            'title': forms.TextInput(
                attrs={'class': 'form-control'}
            ),

            'content': forms.Textarea(
                attrs={
                    'rows': '8',
                    'class': 'form-control'
                }
            ),

            'category': forms.Select(
                attrs={'class': 'form-control'}
            ),

            'tags': forms.SelectMultiple(
                attrs={'class': 'form-control'}
            ),
        }

    def clean_slug(self):
        title = self.cleaned_data.get('title')

        if title and len(title) < 5:
            raise forms.ValidationError(
                'Title must be at least 5 characters long.'
            )

        return title

    def clean(self):
        cleaned_data = super().clean()

        title = cleaned_data.get('title')
        content = cleaned_data.get('content')

        if (
            title
            and content
            and title.lower() in content.lower()[:50]
        ):
            raise forms.ValidationError(
                "Don't repeat the title verbatim at the start of the content."
            )

        return cleaned_data
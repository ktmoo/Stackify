from django import forms
from .models import Post,Comments
from django.core.exceptions import ValidationError

class PostForm(forms.ModelForm):
    class Meta:
        model= Post
        fields=["title","content","tags"]

        widgets={
            "title": forms.TextInput(attrs={'class': "form-control"}),
            "tags": forms.TextInput(attrs={'class': "form-control"}),
            "content": forms.Textarea(attrs={'class': "form-control","width": "100%"}),
        }

    def clean(self):
        cleaned_data=self.cleaned_data
        title=self.cleaned_data["title"]
        if Post.objects.filter(title=title).exists():
            raise ValidationError("Username already exsists!")
        return cleaned_data


class CommentsForm(forms.ModelForm):
    class Meta:
        model= Comments
        fields=["content"]
        widgets={
            "content": forms.TextInput(attrs={'class': "form-control"}),
        }

    def clean(self):
        cleaned_data=self.cleaned_data
        return cleaned_data


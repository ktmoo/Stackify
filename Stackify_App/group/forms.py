from django import forms
from django.core.exceptions import ValidationError
from .models import Group

class GroupForm(forms.Form):
    class Meta:
        model=Group
        fields=['name', 'description']

        widgets={
            "name": forms.TextInput(attrs={'class': "form-control"}),
            "description": forms.TextInput(attrs={'class': "form-control"}),
        }

    def clean(self):
        cleaned_data=self.cleaned_data
        name=self.cleaned_data["name"]
        if Group.objects.filter(name=name).exists():
            raise ValidationError("Username already exsists!")
        return cleaned_data
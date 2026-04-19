from django import forms
from .models import Group, GroupMessage


class GroupForm(forms.ModelForm):
    class Meta:
        model = Group
        fields = ['name', 'description', 'cover']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
        }


class GroupMessageForm(forms.ModelForm):
    class Meta:
        model = GroupMessage
        fields = ['content']
        widgets = {
            'content': forms.TextInput(attrs={'placeholder': 'Type a message...'}),
        }
from django import forms
from django.forms import ModelForm
from chat.models import Room, PrivateRoom

add_labels = {"name": "Room Name"}

class PublicForm(ModelForm):
    username = forms.CharField(max_length=100)
    class Meta:
        model = Room
        fields = ('name',)
        labels = add_labels


class PrivateForm(ModelForm):
    username = forms.CharField(max_length=100)
    class Meta:
        model = PrivateRoom
        fields = ('name', 'password',)
        labels = add_labels
    password = forms.CharField(widget=forms.PasswordInput, max_length=100)


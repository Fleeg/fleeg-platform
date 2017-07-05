from django import forms
from link.models import Post


class URLForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('url',)

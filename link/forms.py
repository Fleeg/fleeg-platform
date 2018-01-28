from django import forms
from link.models import Post, Comment


class URLForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('url',)


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('text',)

from django import forms
from .models import Comment, Reply


class FormPostComment(forms.ModelForm):
    content = forms.CharField(min_length=1, required=True, widget=forms.Textarea(attrs={
        'class': 'form-control custom-control',
        'placeholder': 'Enter new comment here...',
        'rows': 3,
    }), label="")

    class Meta:
        model = Comment
        exclude = ('user',)


class FormReplyToComment(forms.ModelForm):
    content = forms.CharField(min_length=1, required=True, widget=forms.Textarea(attrs={
        'class': 'form-control custom-control',
        'placeholder': 'Post your comment...',
        'rows': 3,
    }), label="")

    class Meta:
        model = Reply
        exclude = ('user', 'comment', 'parent',)

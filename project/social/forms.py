from django import forms
from .models import Comment


class CommentAddForm(forms.ModelForm):
    content = forms.CharField(min_length=1, required=True, widget=forms.Textarea(attrs={
        'class': 'form-control custom-control',
        'placeholder': 'Enter new comment here...',
        'rows': 3,
    }), label="")

    class Meta:
        model = Comment
        exclude = ('user', )

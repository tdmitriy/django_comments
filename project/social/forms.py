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

    comment_id = forms.CharField(widget=forms.HiddenInput, required=True, label="")
    parent_id = forms.CharField(widget=forms.HiddenInput, required=False, label="", initial=None)

    def save(self, commit=True):
        reply = super(FormReplyToComment, self).save(commit=False)
        reply.content = self.cleaned_data.get('content')
        reply.comment_id = self.cleaned_data.get('comment_id')
        reply.parent_id = self.cleaned_data.get('parent_id')

        return reply.save()

    class Meta:
        model = Reply
        exclude = ('user', 'comment', 'parent',)

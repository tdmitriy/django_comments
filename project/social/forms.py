from django import forms
from .models import Comment


class FormPostComment(forms.ModelForm):
    content = forms.CharField(min_length=1, required=True, widget=forms.Textarea(attrs={
        'class': 'form-control custom-control',
        'placeholder': 'Write your comment...',
        'rows': 3,
    }), label="")

    root_id = forms.CharField(widget=forms.HiddenInput, required=False, label="")
    parent_id = forms.CharField(widget=forms.HiddenInput, required=False, label="")

    def clean_root_id(self):
        err = 'Error: root_id field is not an integer.'
        return self.check_field(self.root_id, err)

    def clean_parent_id(self):
        err = 'Error: parent_id field is not an integer.'
        return self.check_field(self.root_id, err)

    @staticmethod
    def check_field(field, error):
        if field is None or 'null' or '':
            field = None
        else:
            try:
                field = int(field)
            except ValueError:
                raise forms.ValidationError(error)
        return field

    class Meta:
        model = Comment
        exclude = ('user', 'parent')

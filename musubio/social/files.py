from django import forms


class CommentForm(forms.Form):
    body = forms.CharField(
        required=True,
        widget=forms.Textarea(
            attrs={
                'placeholder': 'Write a comment...',
                'class': 'form-control input-lg',
            }))
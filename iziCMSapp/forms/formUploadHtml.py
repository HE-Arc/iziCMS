from django import forms

class formUploadHtml(forms.Form):
    pageContent = forms.CharField(widget=forms.Textarea)

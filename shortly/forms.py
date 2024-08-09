from django import forms

class shortly_form(forms.Form):
    url_field = forms.URLField()
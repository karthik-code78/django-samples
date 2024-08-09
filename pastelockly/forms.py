from django import forms;

from pastelockly.models import PasteLock


class pastelockly_form(forms.ModelForm):
    class Meta:
        model = PasteLock
        fields = ["text_field", "password_field", "is_locked"]
        widgets = {
            'text_field': forms.Textarea(attrs={'rows': 10, 'cols': 20}),
            'password_field': forms.PasswordInput(attrs={'minlength': 16, 'maxlength': 16})
        }
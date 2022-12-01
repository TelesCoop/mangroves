from django import forms

from mangmap.models.models import Contact


class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = [
            "firstname",
            "email",
            "country",
            "lastname",
            "subject",
            "message",
        ]

    agree = forms.BooleanField(required=True)

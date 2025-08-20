from django import forms
from phonenumber_field.formfields import PhoneNumberField

from .models import Enquiry


class EnquiryForm(forms.ModelForm):
    name = forms.CharField(
        widget=forms.TextInput(
            attrs={"class": "w-full px-3 py-2 border border-gray-300 rounded-md"}
        )
    )
    email = forms.EmailField(
        widget=forms.EmailInput(
            attrs={"class": "w-full px-3 py-2 border border-gray-300 rounded-md"}
        )
    )
    phone_number = PhoneNumberField(
        widget=forms.TextInput(
            attrs={"class": "w-full px-3 py-2 border border-gray-300 rounded-md"}
        )
    )
    message = forms.CharField(
        widget=forms.Textarea(
            attrs={
                "class": "w-full px-3 py-2 border border-gray-300 rounded-md",
                "rows": 4,
            }
        )
    )

    class Meta:
        model = Enquiry
        fields = ["name", "email", "phone_number", "message"]

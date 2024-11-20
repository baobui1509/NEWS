from django import forms
from myadmin.models import Contact

class ContactForm(forms.ModelForm):
    admin_message = forms.CharField(widget=forms.Textarea, required=False)
    email = forms.EmailField(
        max_length=100,
        required=True,
        widget=forms.EmailInput(attrs={'placeholder': 'Địa chỉ Email'}),
        error_messages={
            'required': "Email không được để trống. Vui lòng nhập địa chỉ email của bạn.",
            'invalid': 'Email không hợp lệ. Vui lòng nhập đúng định dạng.'
        }
    )
    class Meta:
        model = Contact
        fields = ['name', 'email', 'message']
        error_messages = {
            'name': {
                'required': "Tên không được để trống. Vui lòng nhập tên của bạn.",
            },
            'message': {
                'required': "Tin nhắn không được để trống. Vui lòng nhập lời nhắn của bạn.",
            },
        }

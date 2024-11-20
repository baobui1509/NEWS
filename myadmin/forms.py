from django import forms
from myadmin.models import Category, Article, Contact, Tag

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name', 'slug', 'is_homepage', 'status', 'layout']
        error_messages = {
            'name': {
                'required': "Tên không được để trống. Vui lòng nhập tên của bạn.",
            },
            'slug': {
                'required': "Tin nhắn không được để trống. Vui lòng nhập lời nhắn của bạn.",
                'unique': "Slug này đã tồn tại.",
            },
            # 'image': {
            #     'required': "Ảnh không được để trống. Vui lòng chọn ảnh.",
            # },
        }

class ArticleForm(forms.ModelForm):
    tags = forms.ModelMultipleChoiceField(
        queryset=Tag.objects.all(),  # Lấy tất cả các đối tượng Tag từ cơ sở dữ liệu
        widget=forms.CheckboxSelectMultiple,  # Hoặc bạn có thể sử dụng Widget khác nếu cần
        required=False,  # Nếu bạn không yêu cầu tags
    )
    class Meta:
        model = Article
        fields = ['name', 'slug','is_homepage', 'ordering', 'status', 'special', 'publish_date', 'image', 'category', 'content', 'tags']
        error_messages = {
            'name': {
                'required': "Tên không được để trống. Vui lòng nhập tên.",
            },
            'slug': {
                'required': "Tin nhắn không được để trống. Vui lòng nhập slug.",
                'unique': "Slug này đã tồn tại.",
            },
            'image': {
                'required': "Ảnh không được để trống. Vui lòng chọn ảnh.",
            },
            'publish_date': {
                'required': "Ngày không được để trống. Vui lòng chọn ngày.",
            },
            'ordering': {
                'required': "Ordering không được để trống. Vui lòng chọn ordering.",
            },
            'content': {
                'required': "Nội dung không được để trống. Vui lòng nhập nội dung.",
            },
        }

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
    # phone = forms.CharField(
    #     widget=forms.TextInput(attrs={
    #         'placeholder': 'Số điện thoại*',
    #         'type': 'tel', 
    #         'pattern': '[0-9]{10,11}' 
    #     }),
    #     max_length=11,
    #     error_messages={
    #         'required': "Số điện thoại không được để trống. Vui lòng nhập số điện thoại của bạn.",
    #         'invalid': 'Số điện thoại không hợp lệ. Vui lòng nhập đúng định dạng.'
    #     }
    # )
    class Meta:
        model = Contact
        fields = ['name', 'email', 'phone', 'message']
        error_messages = {
            'name': {
                'required': "Tên không được để trống. Vui lòng nhập tên của bạn.",
            },
            'message': {
                'required': "Tin nhắn không được để trống. Vui lòng nhập lời nhắn của bạn.",
            },
            'phone': {
                'required': "Số điện thoại không được để trống. Vui lòng nhập số điện thoại của bạn.",
                'invalid': 'Số điện thoại không hợp lệ. Vui lòng nhập đúng định dạng.'  
            },
        }
        
class TagForm(forms.ModelForm):
    class Meta:
        model = Tag
        fields = ['name', 'slug']
        error_messages = {
            'name': {
                'required': "Tên không được để trống. Vui lòng nhập tên của bạn.",
            },
            'slug': {
                'required': "Tin nhắn không được để trống. Vui lòng nhập lời nhắn của bạn.",
                'unique': "Slug này đã tồn tại.",
            },
        }

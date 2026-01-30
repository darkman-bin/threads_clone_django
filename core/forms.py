from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import Thread, Profile

User = get_user_model()


class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=False, help_text="اختياري")

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Bootstrap classes
        for name, field in self.fields.items():
            field.widget.attrs.setdefault("class", "form-control")


class LoginForm(AuthenticationForm):
    def __init__(self, request=None, *args, **kwargs):
        super().__init__(request=request, *args, **kwargs)
        self.fields["username"].widget.attrs.update({"class": "form-control", "placeholder": "اسم المستخدم"})
        self.fields["password"].widget.attrs.update({"class": "form-control", "placeholder": "كلمة المرور"})


class ThreadForm(forms.ModelForm):
    class Meta:
        model = Thread
        fields = ("content", "image")
        widgets = {
            "content": forms.Textarea(attrs={
                "rows": 3,
                "class": "form-control",
                "placeholder": "وش في بالك؟ اكتب ثريد…",
                "maxlength": "500",
            }),
            "image": forms.ClearableFileInput(attrs={"class": "d-none"}),
        }

    def clean_content(self):
        content = (self.cleaned_data.get("content") or "").strip()
        if not content:
            raise forms.ValidationError("لا يمكن نشر ثريد فارغ.")
        return content


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ("display_name", "bio", "avatar")
        widgets = {
            "display_name": forms.TextInput(attrs={"class": "form-control", "placeholder": "الاسم الظاهر"}),
            "bio": forms.TextInput(attrs={"class": "form-control", "placeholder": "نبذة قصيرة"}),
            "avatar": forms.ClearableFileInput(attrs={"class": "d-none"}),
        }

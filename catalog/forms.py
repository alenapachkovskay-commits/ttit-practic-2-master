from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser, DesignRequest, Category
from .models import validate_image_file

class CustomUserCreationForm(UserCreationForm):
    full_name = forms.CharField(
        max_length=150,
        label='ФИО',
        widget=forms.TextInput(attrs={'placeholder': 'Иванов Иван Иванович'})
    )
    email = forms.EmailField(required=True)
    consent = forms.BooleanField(
        label='Согласие на обработку персональных данных',
        required=True
    )

    class Meta:
        model = CustomUser
        fields = ('username', 'full_name', 'email', 'password1', 'password2')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.full_name = self.cleaned_data['full_name']
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user


class DesignRequestForm(forms.ModelForm):
    plan_image = forms.ImageField(
        validators=[validate_image_file],
        label='План помещения'
    )
    class Meta:
        model = DesignRequest
        fields = ['title', 'description', 'category', 'plan_image']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
        }

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name']